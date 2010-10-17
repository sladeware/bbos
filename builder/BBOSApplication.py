# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSApplication:
    def __init__(self, processes):
        # The list of processes within this application
        self.processes = processes
        assert type(self.processes) is ListType, "processes is not a list type: %s" % self.process
