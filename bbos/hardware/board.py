
__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos.hardware.processor import *
from builder.utils.type_util import *

class Board(Component):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BBOS does not explicitly refer to them."""
    def __init__(self, name, processors=[], processes=[]):
        Component.__init__(self, name)
        # Set and verify the list of processors on this board
        self.processors = verify_list(processors)
        for processor in self.processors:
            assert isinstance(processor, Processor), "processor is not a Processor: %s" % processor

    def get_processors(self):
        return self.processors

    def get_processes(self):
        processes = []
        for processor in self.processors:
            processes += processor.get_processes()
        return processes
