# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSDriver:
    def __init__(self, boot, main, exit, files, name, port, version):
        # The bootstrapper function for this driver
        self.boot = boot
        assert type(self.boot) is StringType, "boot is not a string type: %s" % self.boot

        # This is the main main function for the driver that calls messenger()
        self.main = main
        assert type(self.main) is StringType, "main is not a string type: %s" % self.main

        # The exit function for this driver
        self.exit = exit
        assert type(self.exit) is StringType, "exit is not a string type: %s" % self.exit

        # The driver source files
        self.files = files
        assert type(self.files) is ListType, "files is not a list type: %s" % self.files

        # The unique name of this driver
        self.name = name
        assert type(self.name) is StringType, "name is not a string type: %s" % self.name

        # The port name used for communication with this driver
        self.port = port
        assert type(self.port) is StringType, "port is not a string type: %s" % self.port

        # The version of the driver
        self.version = version
        assert type(self.version) is IntType, "version is not an integer type: %s" % self.version
