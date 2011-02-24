"""Dual core X86 processor.

This processor is a no frills dual core X86 processor intended primarily
for simluation used for rapid prototyping and testing.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.cores.x86 import *
from bbos.hardware.processor import *

class x86x2(Processor):
    def __init__(self, processes=[]):
        cores = []
        for process in processes:
            cores.append(x86(process))
        Processor.__init__(self, "x86x2", cores, num_cores=2)
