"""
Base class used for creating a BBOS processor.

A processor contains one or more cores. It is a discrete semiconductor based
device used for computation. For example, the PIC32MX5 microcontroller is a
processor.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos.hardware.core import Core
from builder.utils.type_util import *

class Processor(Component):
    owner = None
    cores = []

    def __init__(self, name, number_of_cores=1, cores=[]):
        Component.__init__(self, name)
        self.number_of_cores = number_of_cores
        self.cores = [Core("Unknown")] * number_of_cores
        if cores:
            self.set_cores(cores)

    def get_owner(self):
        return self.owner

    def set_owner(self, board):
        # XXX check the board
        self.owner = board
        for process in self.get_processes():
            if process:
                process.hardware.board = board

    def get_number_of_cores(self):
        return self.number_of_cores

    def set_cores(self, cores):
        verify_list(cores)
        for i in range(len(cores)):
            self.set_core(cores[i], i)

    def set_core(self, core, i):
        assert isinstance(core, Core), "core is not a Core: %s" % core
        self.validate_core(core)
        self.validate_core_id(i)
        self.cores[i] = core
        core.set_owner(self)

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplemented

    def is_valid_core(self, core):
        return True

    def validate_core_id(self, i):
        if self.get_number_of_cores() <= i:
            raise NotImplemented, "The %s supports up to %d processes. " \
                "You have too many: %d" % (self.__class__.__name__, self.get_number_of_cores(), i)

    def get_cores(self):
        return self.cores

    def get_processes(self):
        processes = []
        for core in self.cores:
            processes.append(core.get_process())
        return processes

