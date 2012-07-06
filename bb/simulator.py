#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

import multiprocessing
import optparse
import os
import random
import signal
import subprocess
import sys
import tempfile
import time

from bb.app import Application
from bb.app.mapping import Mapping, verify_mapping

class _OutputStream:
    PREFIX_FORMAT = '[%s] '

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        """See number of processes within an application. Do not show process
        identifier if we have less than two processes.
        """
        global _config
        prefix = ''
        if not _config.get_option('multiterminal'):
            # We do not use here get_num_processes() since we may have an
            # execution delay between processes. Thus we will use max possible
            # number of processes, which is number of mappings.
            if Application.get_running_instance().get_num_mappings() > 1:
                mapping = Application.get_running_instance().get_active_mapping()
                prefix = self.PREFIX_FORMAT % mapping.get_name()
            if data != '\n':
                # Print prefix only if we have some data
                self.stream.write(prefix)
        self.stream.write(data)

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class _UnbufferedOutputStream(_OutputStream):
    """This class is a subclass of _OutputStream and handles unbuffered output
    stream. It just does flush() after each write().
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        _OutputStream.write(self, data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class Process(multiprocessing.Process):
    """The process is a one to one mapping, which describes a particular CPU
    core and the particular kernel on it. It represents the life of that kernel:
    from its initialization to the point that it stops executing.

    The process is a subclass of :class:`multiprocessing.Process`.
    """

    def __init__(self, mapping):
        global _config

        def bootstrapper():
            os_class = mapping.get_os_class()
            os = os_class(**mapping.get_build_params())
            os.main()
            os.kernel.start()
            return os

        self.__mapping = mapping
        multiprocessing.Process.__init__(self, target=bootstrapper)
        if _config.get_option("multiterminal"):
            self.tmpdir = tempfile.mkdtemp()
            self.fname = os.path.join(self.tmpdir, str(id(self)))
            self.fh = open(self.fname, "w")

    def get_mapping(self):
        """Return :class:`bb.app.application.Process` instance that runs under
        this process.
        """
        return self.__mapping

    def get_pid(self):
        """Return process PID."""
        return self.pid

    def start(self):
        """Start the process."""
        global _config
        # Save a reference to the current stdout
        old_stdout = sys.stdout
        if _config.get_option("multiterminal"):
            # hm, gnome-terminal -x ?
            term_cmd = ["xterm",
                        "-T", "Mapping '%s'" % self.__mapping.get_name(),
                        "-e", "tail",
                        "-f", self.fname]
            self.term = subprocess.Popen(term_cmd)
            sys.stdout = _UnbufferedOutputStream(self.fh)
            # Need a small delay
            time.sleep(1)
        else:
            sys.stdout = _OutputStream(sys.stdout)
        # Now the stdout has been redirected. Call initial start().
        multiprocessing.Process.start(self)
        # Normalize stdout stream
        sys.stdout = old_stdout
        if _config.get_option('multiterminal'):
            print 'Redirect %d output to %d terminal' % (self.pid, self.term.pid)

    def kill(self):
        """Kill this process. See also :func:`os.kill`."""
        global _config
        if _config.get_option('multiterminal'):
            self.term.terminate()
            self.fh.close()
            os.remove(self.fname)
            os.rmdir(self.tmpdir)
        os.kill(self.pid, signal.SIGTERM)

class _Config(object):
    """Class to wrap simulator functionality.

    Attributes:
    optparser: An instnace of optparse.OptionParser
    argv: The original command line as a list.
    args: The positional command line args left over after parsing the options.
    raw_input_fn: Function used for getting raw user input.
    error_fh: Unexpected errors are printer to this file handle.
    """

    def __init__(self, optparser_class=optparse.OptionParser,
                 raw_input_fn=raw_input,
                 out_fh=sys.stdout,
                 error_fh=sys.stderr):
        self.argv = None
        self.optparser_class = optparser_class
        self.raw_input_fn = raw_input_fn
        self.out_fh = out_fh
        self.error_fh = error_fh
        self.args = {}
        self.options = optparse.Values()
        self.optparser = self._get_optparser()

    def parse_command_line(self, argv=sys.argv):
        self.options, self.args = self.optparser.parse_args(argv[1:])
        if self.options.help:
            self._print_help_and_exit()

    def get_option(self, name, default=None):
        value = getattr(self.options, name, default)
        return value

    def _print_help_and_exit(self, exit_code=2):
        self.optparser.print_help()
        sys.exit(exit_code)

    def _get_optparser(self):
        class Formatter(optparse.IndentedHelpFormatter):
            def format_description(self, description):
                return description, '\n'
        parser = self.optparser_class(usage='%prog [Options]',
                                      formatter=Formatter(),
                                      conflict_handler='resolve')
        parser.add_option('-h', '--help', action='store_true', dest='help',
                          help='Show the help message and exit.')
        parser.add_option("--multiterminal", action="store_true",
                          dest="multiterminal",
                          help="Open each new running mapping a new terminal. "\
                              "Supports Linux.")
        return parser

_config = _Config()

# Captured application instance handled by simulator
_application = None

# All the processes will be stored at shared dict object. Thus each
# process will be able to define the mapping by pid.
_processes = list()

def config():
    return _config

def set_application(application):
    global _application
    # TODO(team): verify application object
    _application = application

def stop():
    """Stop running application."""
    global _processes
    if not Application.running_instance:
        raise
    print "\nStopping application"
    # Very important! We need to terminate all the children in order to close
    # all open pipes. Otherwise we will get "IOError: [Errno 32]: Broken
    # pipe". So look up for workers first and terminate them.
    for process in _processes:
        if process.is_alive():
            print "Kill process %d" % process.pid
            process.kill()
    Application.running_instance = None

def start(application=None):
    """Launch the application. Application will randomly execute mappings
    one by one with specified delay (see
    :func:`set_mappings_execution_interval`).

    .. note::

       The only one application can be executed per session.
    """
    global _processes
    global _application

    if application:
        set_application(application)
    if not _application:
        raise

    print "Start application", _application
    Application.running_instance = _application
    if not _application.get_num_mappings():
        raise Exception("Nothing to run. Please, add at least one mapping "
                        "to this application.")
    # First of all, build an execution order of mappings
    execution_order = range(_application.get_num_mappings())
    random.shuffle(execution_order)
    # Execute mappings one by one by using execution order. Track keyboard
    # interrupts and system exit.
    try:
        for i in execution_order:
            # Take a random mapping
            mapping = _application.get_mappings()[i]
            if not mapping.get_os_class():
                raise Exception('Cannot create OS instance for "%s".' % mapping)
            process = Process(mapping)
            _processes.append(process)
            process.start()
            print "Start process %d" % process.get_pid()
            # Check for delay. Sleep for some time before the
            # next mapping will be executed.
            time.sleep(_application.get_mappings_execution_interval())
        # Wait for each process
        for process in _processes:
            process.join()
    except KeyboardInterrupt, e:
        stop()
    except SystemExit, e:
        stop()
