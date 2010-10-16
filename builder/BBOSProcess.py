# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSCompiler
from types import *

class BBOSProcess:
    # The IPC files used to add the IPC part
    __ipc_files = None

    # The compiler object for this process
    compiler = None
    
    # The list of BBOSDrivers within this process
    drivers = None

    # The list of process source files used for the build
    files = None

    # IPC is used by this process
    ipc = None

    # List of ports
    ports = None

    # The list of entry functions for each thread
    threads = None

    def __init__(self, c, d, f, i, p, t):
        compiler = c
        assert isinstance(compiler, BBOSCompiler.BBOSCompiler), "compiler is not a BBOSCompiler type"
        drivers = d
        assert type(drivers) is ListType, "drivers is not a list type: %s" % drivers
        files = f
        assert type(files) is ListType, "files is not a list type: %s" % files
        ipc = i
        assert type(ipc) is BooleanType, "ipc is not a boolean type: %s" % ipc
        ports = p
        assert type(ports) is ListType, "ports is not a list type: %s" % ports
        threads = t
        assert type(threads) is ListType, "threads is not a list type: %s" % threads
