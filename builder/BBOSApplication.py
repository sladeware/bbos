# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSApplication:
    def __init__(self, p):
        # The list of processes within this application
        self.processes = p
        assert type(self.processes) is ListType, "processes is not a list type: %s" % process
