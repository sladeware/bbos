"""
Base class used to represent a core within a processor.

A Core is the smallest computational unit supported by BBOS. There is one
core per processes and one process per core.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos.kernel import Kernel

class Core(Component):
    def __init__(self, name, process):
        self.name = name
        # The process running on this core
        self.set_process(process)

    def get_name(self):
        return self.name

    def set_process(self, process):
        assert isinstance(process, Kernel), "process is not a Kernel: %s" % process
        self.process = process

    def get_process(self):
        return self.process


