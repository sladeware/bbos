# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#
# A Core is the smallest computational unit supported by BBOS. There is one
# core per processes and one process per core.
#

from bbos_process import *
from common import *


class BBOSCore:
    def __init__(self, process):
        # The process running on this core
        assert isinstance(process, BBOSProcess), "process is not a BBOSProcess: %s" % process
        self.process = process
