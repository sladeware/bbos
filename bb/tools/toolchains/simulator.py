#!/usr/bin/env python

import imp
import multiprocessing
import sys
import warnings

import bb
from bb.config import host_os
from bb.tools.toolchains.toolchain import Toolchain

# TODO: do not ignore every single warning
#warnings.simplefilter("ignore")

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
    def __init__(self, ):

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
        """Kill this process. See also :func:`host_os.kill`."""
        host_os.kill(self.pid, signal.SIGTERM)

class SimulationToolchain(Toolchain):
    def __init__(self, *args, **kargs):
        Toolchain.__init__(self, *args, **kargs)
        # All the processes will be stored at shared dict object. Thus
        # each process will be able to define the mapping by pid.
        self._processes = list()

    def get_num_processes(self):
        """Return number of running processes."""
        return len(self._processes)

    def _build(self, *args, **kargs):
        # Load files
        #import py_compile
        #print py_compile.main(self.get_sources())
        import subprocess
        print ["python",] + self.get_sources()
        subprocess.call(["python",] + self.get_sources())


    def _start_simulation(self, runtime_os_class, buildtime_os):
        print "Start simulation"
        process = Process(runtime_os_class, buildtime_os)
        self._processes.append(process)
        process.start()
        print 'Start simulation OS as process %d' \
            % (process.get_pid(),)

    def _get_package_name_by_file_name(self, file_name):
        package_name = None
        for home in (host_os.environ['BB_HOME'], host_os.environ['BB_PACKAGE_HOME']):
            if file_name.startswith(home):
                package_name = file_name[len(home):]
                package_name = package_name.strip(host_os.sep)
                package_name, _ = host_os.path.splitext(package_name)
                package_name = package_name.replace(host_os.sep, '.')
                return package_name
        raise Exception()
