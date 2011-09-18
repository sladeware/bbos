#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Parallax Propeller P8X32A processor.

The Parallax Propeller P8X32A family of microcontrollers contains eight cogs 
(a.k.a BBOS cores). Its system clock runs up to 80MHz.

The processor contains 32K RAM and 32K ROM globally that all cogs share using a 
multiplexed system bus. There are 32 IO pins."""

from bb.os.hardware import Processor
from bb.os.hardware.cores import PropellerCog
from bb.utils.type_check import verify_list

class PropellerP8X32A(Processor):
    def __init__(self, processes=[]):
        verify_list(processes)
        cores = [PropellerCog()]
        for process in processes:
            cores.append(PropellerCog(process))
        Processor.__init__(self, "Propeller P8X32A", 8, cores)

import bb.os.hardware.processors.propeller_p8x32a.setup
