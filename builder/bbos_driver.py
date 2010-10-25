# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# A BBOS driver is a special type of thread that has a well defined
# interface designed to support hardware.
#

from common import *


class BBOSDriver:
    def __init__(self, boot, main, exit, files, name, ports, version):
        # The bootstrapper function for this driver
        self.boot = verify_string(boot)

        # This is the main main function for the driver that calls messenger()
        self.main = verify_string(main)

        # The exit function for this driver
        self.exit = verify_string(exit)

        # The driver source files
        self.files = verify_list(files)

        # The unique name of this driver
        self.name = verify_string(name)

        # The ports used for communication with this driver
        self.ports = verify_list(ports)

        # The version of the driver
        self.version = verify_int(version)
