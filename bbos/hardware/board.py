"""Base class representing a board -- i.e. computing hardware.

A board contains one or more processors. Each processor may or may not be
the same, depending on the board. A board is a piece of hardware that
performs computation within its processors. Other supporting hardware
may be present on the board, but BBOS does not explicitly refer to them.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos_processor import *
from common import *


class BBOSBoard:
    def __init__(self, processors):
        # The list of processors on this board
        self.processors = verify_list(processors)
        for processor in self.processors:
            assert isinstance(processor, BBOSProcessor), "processor is not a BBOSProcessor: %s" % processor

    def get_processes(self):
        processes = []
        for processor in self.processors:
            processes += processor.get_processes()
        return processes
