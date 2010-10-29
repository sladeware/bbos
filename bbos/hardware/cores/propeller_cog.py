"""Parallax Propeller processor's cog core.

A "cog" is a CPU contained within the Propeller processor. Cogs are designed
to run independently and concurrently within the same silicon die. They have
their own internal memory, configurable counters, video generators and access
to I/O pins as well as the system clock. All the cogs in the processor share
access to global resources sych as the main RAM/ROM, synchronization resources
and specialized monitoring capabilities to know what the other cogs are doing.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.core import *
from bbos.builder.common import *


class PropellerCog(BBOSCore):
    def __init__(self, process, memsize):
        BBOSCore.__init__(self, process)

        verify_int(memsize)
        self.memsize = memsize
        assert self.memsize <= 32, "memsize must be no greater than 32KB: %d" % self.memsize

        # Modify includes
        self.process.append_include_files("propeller_demo_board.h")

        # Modify compiler include directories
        dirs = []
        self.modify_compiler_include_directories(dirs)

        # Modify compiler include argument
        self.modify_compiler_include_argument("-I")

        # Modify compiler name
        self.modify_compiler_name("catalina")

        # Modify compiler options
        options = "-DDEMO -m " + str(self.memsize)

