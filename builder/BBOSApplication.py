# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from types import *

class BBOSApplication:
    # The list of processes within this application
    processes = None

    def __init__(self, p):
        processes = p
        assert type(processes) is ListType, "processes is not a list type: %s" % process
