# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSDriver:
    def __init__(self, bf, ef, exf, f, n, p, v):
        # The bootstrapper function for this driver
        self.boot_function = bf
        assert type(self.boot_function) is StringType, "boot_function is not a string type: %s" % self.boot_function

        # This is the main entry function for the driver that calls messenger()
        self.entry_function = ef
        assert type(self.entry_function) is StringType, "entry_function is not a string type: %s" % self.entry_function

        # The exit function for this driver
        self.exit_function = exf
        assert type(self.exit_function) is StringType, "exit_function is not a string type: %s" % self.exit_function

        # The driver source files
        self.files = f
        assert type(self.files) is ListType, "files is not a list type: %s" % self.files

        # The unique name of this driver
        self.name = n
        assert type(self.name) is StringType, "name is not a string type: %s" % self.name

        # The port name used for communication with this driver
        self.port = p
        assert type(self.port) is StringType, "port is not a string type: %s" % self.port

        # The version of the driver
        self.version = v
        assert type(self.version) is IntType, "version is not an integer type: %s" % self.version
