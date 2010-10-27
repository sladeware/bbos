"""Class used to represent a single context of execution within BBOS.

A process is executable software running in its own context of execution on a
core. A process contains threads, which are time shared on the same core
in a cooperatively scheduled non-preemptive manner.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos_compiler import *
from common import *


class BBOSProcess:
    def __init__(self, compiler, drivers, files, ipc, mempools, ports, static_scheduler, threads):
        # The include files used by this process
        self.__includes = []

        # The IPC files used to add the IPC part
        self.__ipc_files = []

        # The compiler object for this process
        assert isinstance(compiler, BBOSCompiler), "compiler is not a BBOSCompiler: %s" % compiler
        self.compiler = compiler

        # The list of BBOSDrivers within this process
        self.drivers = verify_list(drivers)

        # The list of process source files used for the build
        self.files = verify_list(files)

        # IPC is used by this process
        self.ipc = verify_boolean(ipc)

        # List of ports
        self.mempools = verify_list(mempools)

        # List of ports
        self.ports = verify_list(ports)

        # Choice of static scheduler or default
        self.static_scheduler = verify_boolean(static_scheduler)

        # The list of entry functions for each thread
        self.threads = verify_list(threads)

        # Add the system threads to this process
        self.add_system_threads()

    def add_system_threads(self):
        # Always add the system idle thread
        self.threads.append("bbos_idle")

        # Add IPC system thread to this process
        if self.ipc:
            self.threads.append("bbos_ipc") 

    def append_include_files(self, name):
        verify_string(name)
        self.__includes.append(name)

    def get_include_files(self):
        return self.__includes
