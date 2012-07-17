#!/usr/bin/env python

import imp
import multiprocessing
import os
import sys
import warnings

from bb.build.toolchains.toolchain import Toolchain

# TODO: do not ignore every single warning
warnings.simplefilter("ignore")

class _OutputStream:
    PREFIX_FORMAT = '[%s] '

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        """See number of processes within an application. Do not show process
        identifier if we have less than two processes.
        """
        prefix = ''
        # TODO: fix this
        #if not _config.get_option('multiterminal'):
        #    # We do not use here get_num_processes() since we may have an
        #    # execution delay between processes. Thus we will use max possible
        #    # number of processes, which is number of mappings.
        #    if Application.get_running_instance().get_num_mappings() > 1:
        #        mapping = Application.get_running_instance().get_active_mapping()
        #        prefix = self.PREFIX_FORMAT % mapping.get_name()
        #    if data != '\n':
        #        # Print prefix only if we have some data
        #        self.stream.write(prefix)
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
    def __init__(self, sim_os_class, os):

        def bootstrapper():
            sim_os = sim_os_class(os)
            sim_os.main()
            return sim_os

        multiprocessing.Process.__init__(self, target=bootstrapper)

    def get_pid(self):
        """Return process PID."""
        return self.pid

    def start(self):
        """Start the process."""
        # Save a reference to the current stdout
        old_stdout = sys.stdout
        sys.stdout = _OutputStream(sys.stdout)
        # Now the stdout has been redirected. Call initial start().
        multiprocessing.Process.start(self)
        # Normalize stdout stream
        sys.stdout = old_stdout

    def kill(self):
        """Kill this process. See also :func:`os.kill`."""
        os.kill(self.pid, signal.SIGTERM)

class Simulator(Toolchain):
    def __init__(self, *args, **kargs):
        Toolchain.__init__(self, *args, **kargs)
        # All the processes will be stored at shared dict object. Thus
        # each process will be able to define the mapping by pid.
        self._processes = list()

    def get_num_processes(self):
        """Return number of running processes."""
        return len(self._processes)

    def _build(self, *args, **kargs):
        # Find os class
        buildtime_os = kargs.get("os", None)
        if not buildtime_os:
            print "os instance wasn't pass"
            return
        # Load files
        # TODO: check os_class from mapping
        buildtime_os_class = 'OS'
        runtime_os_class = None
        for source in self.get_sources():
            package_name = self._get_package_name_by_file_name(source)
            if source.startswith(os.environ['BB_APPLICATION_HOME']):
                package_name = source[len(os.environ['BB_APPLICATION_HOME']):]
                package_name, _ = os.path.splitext(package_name)
                package_name = package_name.replace(os.sep, '.')
                package_name = "bb.runtime.application" + package_name
            print 'Import "%s" as "%s"' % (source, package_name)
            mod = None
            try:
                mod = __import__(package_name, globals(), locals(), [], -1)
            except ImportError, e:
                try:
                    mod = imp.load_source(package_name, source)
                except RuntimeWarning, e:
                    pass
            if not mod:
                raise ImportError("Module cannot be load")
            # TODO: fix this. See TODO on above.
            if not runtime_os_class and getattr(mod, buildtime_os_class, None):
                runtime_os_class = getattr(mod, buildtime_os_class)
        if not runtime_os_class:
            print "Cannot build this mapping. OS class '%s' cannot be found." % buildtime_os_class
            return
        self._start_simulation(runtime_os_class, buildtime_os)

    def _start_simulation(self, runtime_os_class, buildtime_os):
        print "Start simulation"
        process = Process(runtime_os_class, buildtime_os)
        self._processes.append(process)
        process.start()
        print 'Start simulation OS as process %d' \
            % (process.get_pid(),)

    def _get_package_name_by_file_name(self, file_name):
        package_name = None
        for home in (os.environ['BB_HOME'], os.environ['BB_PACKAGE_HOME']):
            if file_name.startswith(home):
                package_name = file_name[len(home):]
                package_name = package_name.strip(os.sep)
                package_name, _ = os.path.splitext(package_name)
                package_name = package_name.replace(os.sep, '.')
                return package_name
        raise Exception()
