#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Parallax Propeller P8X32A processor.

The Parallax Propeller P8X32A family of microcontrollers contains eight cogs 
(a.k.a BBOS cores). Its system clock runs up to 80MHz.

The processor contains 32K RAM and 32K ROM globally that all cogs share using a 
multiplexed system bus. There are 32 IO pins."""

from bb.hardware import Processor
from bb.hardware.cores import PropellerCog
from bb.utils.type_check import verify_list

class PropellerP8X32A(Processor):
    driver="bb.os.drivers.processors.propeller_p8x32"

    def __init__(self, mappings=[]):
        verify_list(mappings)
        cores = [PropellerCog()]
        for mapping in mappings:
            cores.append(PropellerCog(mapping))
        Processor.__init__(self, "Propeller P8X32A", 8, cores)

