
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component
from bbos.hardware.processor import *
from builder.utils.type_util import *

class Board(Component):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BBOS does not explicitly refer to them."""

    processors = []

    def __init__(self, name, number_of_processors, processors=[]):
        Component.__init__(self, name)
        # Set and verify the list of processors on this board
        self.number_of_processors = number_of_processors
        # Setup processors
        # By default if list of processors was not defined will be created a list
        # of Processor instances.
        self.processors = [Processor("Unknown")] * number_of_processors
        if processors:
            self.set_processors(processors)

    def set_processors(self, processors):
        verify_list(processors)
        for i in range(len(processors)):
            self.set_processor(processors[i], i)

    def set_processor(self, processor, i=0):
        """Set a processor with specified identifier."""
        assert isinstance(processor, Processor), "processor is not a Processor: %s" % processor
        self.validate_processor(processor)
        self.validate_processor_id(i)
        processor.set_owner(self)
        self.processors[i] = processor

    def get_processes(self):
        """Collect and return processes from all processors."""
        processes = []
        for processor in self.get_processors():
            processes.extend(processor.get_processes())
        return processes

    def get_processor(self, i=0):
        self.validate_processor_id(i)
        return self.processors[i]

    def validate_processor_id(self, n):
        if self.get_number_of_processors() < n:
            raise NotImplemented

    def validate_processor(self, processor):
        if not self.is_valid_processor(processor):
            raise NotImplemented

    def is_valid_processor(self, processor):
        return True

    def get_number_of_processors(self):
        return self.number_of_processors

    def get_processors(self):
        return self.processors

    def get_processes(self):
        processes = []
        for processor in self.processors:
            processes += processor.get_processes()
        return processes
