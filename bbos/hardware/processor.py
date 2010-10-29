"""
Base class used for creating a BBOS processor.

A processor contains one or more cores. It is a discrete semiconductor based
device used for computation. For example, the PIC32MX5 microcontroller is a
processor.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.builder.common import *
from bbos.hardware.core import *


class BBOSProcessor:
    def __init__(self, cores):
        # The list of cores within this processor
        self.cores = verify_list(cores)
        for core in self.cores:
            assert isinstance(core, BBOSCore), "core is not a BBOSCore: %s" % core

    def get_processes(self):
        processes = []
        for core in self.cores:
            processes.append(core.process)
        return processes
