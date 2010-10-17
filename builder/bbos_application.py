# 
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

from common import *

class BBOSApplication:
    def __init__(self, processes):
        # The list of processes within this application
        self.processes = verify_list(processes)

