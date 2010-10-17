# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from common import *

class BBOSDriver:
    def __init__(self, boot, main, exit, files, name, port, version):
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

        # The port name used for communication with this driver
        self.port = verify_string(port)

        # The version of the driver
        self.version = verify_int(version)
