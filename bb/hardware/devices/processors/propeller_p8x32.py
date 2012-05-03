#!/usr/bin/env python

"""The Parallax P8X32A Propeller chip is a multi-core architecture parallel
microcontroller with eight 32-bit RISC CPU cores.

Each of the eight 32-bit cores (called a cog) has a CPU which has access to 512
32-bit long words (2 KB) of instructions and data."""

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"

from bb.hardware.devices import Pin
from bb.hardware.devices.processors import Processor
from bb.utils.type_check import verify_list

#_______________________________________________________________________________

class PropellerP8X32A(Processor):
    """Parallax Propeller P8X32A processor.

    The Parallax Propeller P8X32A family of microcontrollers contains eight cogs
    (a.k.a BBOS cores). Its system clock runs up to 80MHz.

    The processor contains 32K RAM and 32K ROM globally that all cogs share
    using a multiplexed system bus. There are 32 IO pins."""

    class Core(Processor.Core):
        """Parallax Propeller processor's cog core.

        A "cog" is a CPU contained within the Propeller processor. Cogs are
        designed to run independently and concurrently within the same silicon
        die. They have their own internal memory, configurable counters, video
        generators and access to I/O pins as well as the system clock. All the
        cogs in the processor share access to global resources sych as the main
        RAM/ROM, synchronization resources and specialized monitoring
        capabilities to know what the other cogs are doing."""

        def __init__(self, mapping=None):
            Processor.Core.__init__(self, mapping)

    Cog = Core

    def __init__(self, mappings=[]):
        verify_list(mappings)
        cores = [self.Core()]
        for mapping in mappings:
            cores.append(self.Core(mapping))
        Processor.__init__(self, 8, cores)
        self.metadata.name = "PROPELLER_P8X32"

    def __str__(self):
        return "Propeller P8X32A"

class PropellerP8X32A_Q44(PropellerP8X32A):
    """The P8X32A-Q44 is most useful for prototyping in its 44-pin QFP
    package."""
