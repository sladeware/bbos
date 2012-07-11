#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simulation toolchain."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Alexander Sviridenko <oleks.sviridenko@gmail.com>"

from bb.builder import toolchain_manager
from bb.builder.toolchains.toolchain import Toolchain

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

    def __init__(self, mapping, os_class):
        global _config

        self.__mapping = mapping
        self.__os_class = os_class

        def bootstrapper():
            os = os_class() # TODO:  add build_params
            os.main()
            os.kernel.start()
            return os

        multiprocessing.Process.__init__(self, target=bootstrapper)
        if _config.get_option("multiterminal"):
            self.tmpdir = tempfile.mkdtemp()
            self.fname = os.path.join(self.tmpdir, str(id(self)))
            self.fh = open(self.fname, "w")

    def get_mapping(self):
        return self.__mapping

    def get_os_class(self):
        return self.__os_class

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
                        "-T", "OS '%s'" % self.__os_class,
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

@toolchain_manager.toolchain
class SimulationToolchain(Toolchain):
    """This toolchain provides simulation support."""

    def __init__(self):
        # All the processes will be stored at shared dict object. Thus
        # each process will be able to define the mapping by pid.
        self.__processes = list()

    def get_active_mapping(self):
        """Return currently running :class:`bb.app.mapping.Mapping` instance."""
        process = multiprocessing.current_process()
        #print >>sys.stderr, self.__processes
        #if not process in self.__processes:
        #    raise Exception("Cannot identify %d" % process.pid)
        return process.get_mapping()

    def get_num_processes(self):
        """Return number of running processes."""
        return len(self.__processes)
    
    def build(self, *args, **kargs):
        print "Start simulation"
                #process = Process(mapping, os_class)
                #_processes.append(process)
                #process.start()
                #print 'Start simulation process %d for core "%s"' \
                #    % (process.get_pid(), core)

    def stop(self):
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
