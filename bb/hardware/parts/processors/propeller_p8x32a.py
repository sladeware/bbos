#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Parallax Propeller P8X32A processor.

The Parallax Propeller P8X32A family of microcontrollers contains eight cogs
(a.k.a BBOS cores). Its system clock runs up to 80MHz.

The processor contains 32K RAM and 32K ROM globally that all cogs share using a
multiplexed system bus. There are 32 IO pins."""

from bb.hardware.parts import Processor
from bb.utils.type_check import verify_list

class PropellerCog(Core):
    """Parallax Propeller processor's cog core.

    A "cog" is a CPU contained within the Propeller processor. Cogs
    are designed to run independently and concurrently within the same
    silicon die. They have their own internal memory, configurable
    counters, video generators and access to I/O pins as well as the
    system clock. All the cogs in the processor share access to global
    resources sych as the main RAM/ROM, synchronization resources and
    specialized monitoring capabilities to know what the other cogs
    are doing."""

    def __init__(self, mapping=None):
        Core.__init__(self, "Propeller Cog", mapping)

class PropellerP8X32A(Processor):
    driver="bb.os.drivers.processors.propeller_p8x32"

    def __init__(self, mappings=[]):
        verify_list(mappings)
        cores = [PropellerCog()]
        for mapping in mappings:
            cores.append(PropellerCog(mapping))
        Processor.__init__(self, "PROPELLER_P8X32", 8, cores)

    def __str__(self):
        return "Propeller P8X32A"
