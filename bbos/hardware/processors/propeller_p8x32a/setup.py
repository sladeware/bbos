
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.cores import PropellerCog
from bbos.hardware.processor import *
from builder.utils.type_util import *

class PropellerP8X32A(Processor):
    """Parallax Propeller P8X32A processor.

    The Parallax Propeller P8X32A family of microcontrollers contains
    eight cogs (a.k.a BBOS cores). Its system clock runs up to 80MHz.
    The processor contains 32K RAM and 32K ROM globally that all cogs
    share using a multiplexed system bus. There are 32 IO pins."""
    def __init__(self, processes=[]):
        verify_list(processes)
        cores = []
        for process in processes:
            cores.append(PropellerCog(process))
        Processor.__init__(self, "Propeller P8X32A", 8, cores)

