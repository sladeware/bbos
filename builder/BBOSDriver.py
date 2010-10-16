# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSDriver:
    # The bootstrapper function for this driver
    boot_function = None
    
    # This is the main entry function for the driver that calls messenger()
    entry_function = None

    # The exit function for this driver
    exit_function = None

    # The driver source files
    files = None

    # The unique name of this driver
    name = None

    # The port name used for communication with this driver
    port = None

    # The version of the driver
    version = None

    def __init__(self, bf, ef, exf, f, n, p, v):
        boot_function = bf
        assert type(boot_function) is StringType, "boot_function is not a string type: %s" % boot_function
        entry_function = ef
        assert type(entry_function) is StringType, "entry_function is not a string type: %s" % entry_function
        exit_function = exf
        assert type(exit_function) is StringType, "exit_function is not a string type: %s" % exit_function
        files = f
        assert type(files) is ListType, "files is not a list type: %s" % files
        name = n
        assert type(name) is StringType, "name is not a string type: %s" % name
        port = p
        assert type(port) is StringType, "port is not a string type: %s" % port
        version = v
        assert type(version) is IntType, "version is not an integer type: %s" % version
