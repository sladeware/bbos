"""Base class used to represent a core within a processor.

A Core is the smallest computational unit supported by BBOS. There is one
core per processes and one process per core."""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos import BBOS

class Core(Component):
    owner = None
    process = None

    def __init__(self, name, process=None):
        Component.__init__(self, name)
        # The process running on this core
        if process:
            self.set_process(process)

    def get_owner(self):
        return self.owner

    def set_owner(self, processor):
        # XXX check the processor
        self.owner = processor
        if self.get_process():
            self.get_process().hardware.processor = processor

    def set_process(self, process):
        assert isinstance(process, BBOS), "process is not a BBOS: %s" % process
        self.process = process
        process.hardware.core = self

    def get_process(self):
        return self.process


