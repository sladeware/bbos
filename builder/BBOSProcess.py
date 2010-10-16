# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSCompiler
from types import *

class BBOSProcess:
    def __init__(self, c, d, f, i, p, t):
        # The IPC files used to add the IPC part
        self.__ipc_files = None
        
        # The compiler object for this process
        self.compiler = c
        assert isinstance(self.compiler, BBOSCompiler.BBOSCompiler), "compiler is not a BBOSCompiler type"

        # The list of BBOSDrivers within this process
        self.drivers = d
        assert type(self.drivers) is ListType, "drivers is not a list type: %s" % drivers

        # The list of process source files used for the build
        self.files = f
        assert type(self.files) is ListType, "files is not a list type: %s" % files

        # IPC is used by this process
        self.ipc = i
        assert type(self.ipc) is BooleanType, "ipc is not a boolean type: %s" % ipc

        # List of ports
        self.ports = p
        assert type(self.ports) is ListType, "ports is not a list type: %s" % ports

        # The list of entry functions for each thread
        self.threads = t
        assert type(self.threads) is ListType, "threads is not a list type: %s" % threads
