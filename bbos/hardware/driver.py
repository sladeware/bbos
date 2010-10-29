"""Class used to represent a driver thread within BBOS.

A BBOS driver is a special type of thread that has a well defined
interface designed to support hardware.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.builder.common import *


class BBOSDriver:
    def __init__(self, files, name, ports, version):
        # The driver source files
        self.files = verify_list(files)

        # The unique name of this driver
        self.name = verify_string(name)

        # The ports used for communication with this driver
        self.ports = verify_list(ports)

        # The version of the driver
        self.version = verify_int(version)
