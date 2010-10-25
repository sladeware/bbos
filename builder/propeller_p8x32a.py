# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# The Parallax Propeller P8X32A family of microcontrollers contains
# eight cogs (a.k.a BBOS cores). Its system clock runs up to 80MHz.
# The processor contains 32K RAM and 32K ROM globally that all cogs
# share using a multiplexed system bus. There are 32 IO pins.
#

from bbos_processor import *
from common import *
from propeller_cog import *


class PropellerP8X32A(BBOSProcessor):
    def __init__(self, processes, memsize):
        verify_list(processes)
        number_of_processes = len(processes)
        assert number_of_processes <= 8, "The P8X32A supports up to 8 processes. You have too many: %d" % number_of_processes

        cores = []
        for process in processes:
            cores.append(PropellerCog(process, memsize))

        BBOSProcessor.__init__(self, cores)

