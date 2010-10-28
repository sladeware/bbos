"""Parallax Propeller processor's cog core.

A "cog" is a CPU contained within the Propeller processor. Cogs are designed
to run independently and concurrently within the same silicon die. They have
their own internal memory, configurable counters, video generators and access
to I/O pins as well as the system clock. All the cogs in the processor share
access to global resources sych as the main RAM/ROM, synchronization resources
and specialized monitoring capabilities to know what the other cogs are doing.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from lib.bbos_core import *
from lib.common import *


class PropellerCog(BBOSCore):
    def __init__(self, process, memsize):
        BBOSCore.__init__(self, process)

        verify_int(memsize)
        self.memsize = memsize
        assert self.memsize <= 32, "memsize must be no greater than 32KB: %d" % self.memsize

        # Modify includes
        self.process.append_include_files("propeller_demo_board.h")

        # Modify compiler include directories
        if self.process.compiler.includes:
            print "WARNING: Overwriting preexisting compiler include directories"
        self.process.compiler.includes = []

        # Modify compiler include argument
        if self.process.compiler.include_argument:
            print "WARNING: Overwriting preexisting compiler include argument"
        self.process.compiler.include_argument = "-I"

        # Modify compiler name
        if self.process.compiler.name:
            print "WARNING: Overwriting preexisting compiler name"
        self.process.compiler.name = "catalina"

        # Modify compiler options
        if self.process.compiler.options:
            print "WARNING: Overwriting preexisting compiler options"
        self.process.compiler.options = "-DDEMO -m " + str(self.memsize)
