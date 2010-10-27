"""This class builds the BBOS application code, producing process binaries.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from common import *


class BuildCode:
    def __init__(self, directory, process):
        # The process we're genearting code for
        self.process = process

    def build(self):
        print "Building code..."
