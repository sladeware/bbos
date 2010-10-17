# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from bbos_process import *
from common import *

class BBOSBoard:
    def __init__(self, process):
        assert isinstance(process, BBOSProcess), "process is not a BBOSProcess: %s" % process
        self.process = process


