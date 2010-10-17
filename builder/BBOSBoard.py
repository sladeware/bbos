# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

import BBOSProcess
from types import *

class BBOSBoard:
    def __init__(self, process):
        self.process = process
        assert isinstance(self.process, BBOSProcess.BBOSProcess), "process is not a BBOSBoard: %s" % self.process

