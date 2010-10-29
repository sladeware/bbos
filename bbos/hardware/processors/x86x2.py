"""Dual core X86 processor.

This processor is a no frills dual core X86 processor intended primarily
for simluation used for rapid prototyping and testing.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.cores.x86 import *
from bbos.hardware.processor import *
from bbos.builder.common import *


class X86X2(BBOSProcessor):
    def __init__(self, processes):
        verify_list(processes)
        self.assert_num_processes(len(processes), 2)

        cores = []
        for process in processes:
            cores.append(X86(process))

        BBOSProcessor.__init__(self, cores)
