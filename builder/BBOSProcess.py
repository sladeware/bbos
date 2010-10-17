# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSCompiler
from types import *

class BBOSProcess:
    def add_system_threads(self):
        # Always add the system idle thread
        self.threads.append("bbos_idle")

        # Add IPC system thread to this process
        if self.ipc:
            self.threads.append("bbos_ipc") 

    def get_include_files(self):
        return self.__includes

    def append_include_files(self, name):
        assert type(name) is StringType, "name is not a string type: %s" % name
        self.__includes.append(name)

    def __init__(self, compiler, drivers, files, ipc, mempools, ports, threads):
        # The include files used by this process
        self.__includes = []

        # The IPC files used to add the IPC part
        self.__ipc_files = []

        # The compiler object for this process
        self.compiler = compiler
        assert isinstance(self.compiler, BBOSCompiler.BBOSCompiler), "compiler is not a BBOSCompiler type: %s" % self.compiler

        # The list of BBOSDrivers within this process
        self.drivers = drivers
        assert type(self.drivers) is ListType, "drivers is not a list type: %s" % self.drivers

        # The list of process source files used for the build
        self.files = files
        assert type(self.files) is ListType, "files is not a list type: %s" % self.files

        # IPC is used by this process
        self.ipc = ipc
        assert type(self.ipc) is BooleanType, "ipc is not a boolean type: %s" % self.ipc

        # List of ports
        self.mempools = mempools
        assert type(self.mempools) is ListType, "mempools is not a list type: %s" % self.mempools

        # List of ports
        self.ports = ports
        assert type(self.ports) is ListType, "ports is not a list type: %s" % self.ports

        # The list of entry functions for each thread
        self.threads = threads
        assert type(self.threads) is ListType, "threads is not a list type: %s" % self.threads

        self.add_system_threads()
