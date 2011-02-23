"""
Base class used for creating a BBOS processor.

A processor contains one or more cores. It is a discrete semiconductor based
device used for computation. For example, the PIC32MX5 microcontroller is a
processor.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"
__revision__ = ""

from bbos.hardware.core import Core

class Processor:
    def __init__(self, cores, num_cores=1):
        self.num_cores = num_cores
        assert len(cores) <= num_cores, "The %s supports up to %d processes. " \
        "You have too many: %d" % (self.__class__.__name__, num_cores, len(cores))
        self.cores = cores
        for core in self.cores:
            assert isinstance(core, Core), "core is not a Core: %s" % core

    def get_cores(self):
        return self.cores

    def get_processes(self):
        processes = []
        for core in self.cores:
            processes.append(core.get_process())
        return processes

