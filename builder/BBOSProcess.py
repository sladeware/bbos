from types import *

class BBOSProcess:
    # The IPC files used to add the IPC part
    __ipc_files = None

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

    def __init__(d, f, i, p, t):
        drivers = d
        assert type(drivers) is ListType, "drivers is not a list type"
        files = f
        assert type(files) is ListType, "files is not a list type"
        ipc = i
        assert type(ipc) is BooleanType, "ipc is not a boolean type"
        ports = p
        assert type(ports) is ListType, "ports is not a list type"
        threads = t
        assert type(threads) is ListType, "threads is not a list type"
