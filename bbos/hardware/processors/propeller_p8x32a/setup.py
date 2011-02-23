"""Parallax Propeller P8X32A processor.

The Parallax Propeller P8X32A family of microcontrollers contains
eight cogs (a.k.a BBOS cores). Its system clock runs up to 80MHz.
The processor contains 32K RAM and 32K ROM globally that all cogs
share using a multiplexed system bus. There are 32 IO pins.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.cores import PropellerCog
from bbos.hardware.processor import *

class PropellerP8X32A(Processor):
    def __init__(self, processes):
        cores = []
        for process in processes:
            cores.append(PropellerCog(process))
        Processor.__init__(self, cores, num_cores=8)

