"""Base class used to represent a core within a processor.

A Core is the smallest computational unit supported by BBOS. There is one
core per processes and one process per core.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.bbos_process import *
from bbos.builder.common import *


class BBOSCore:
    def __init__(self, process):
        # The process running on this core
        assert isinstance(process, BBOSProcess), "process is not a BBOSProcess: %s" % process
        self.process = process
