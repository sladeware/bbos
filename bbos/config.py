"""Class used to generate C source code used by BBOS for late binding.

Generate the source code for the bbos.h header file used to late bind BBOS
processes, threads and etc just before building. We need this since the
C macro language is seriously underpowered for our purposes.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import traceback
from types import *

from bbos.project import Project

class Config:
    pass

class Configurable:
    def config(self, proj):
        if not isinstance(proj, Project):
            print "The project instance should based on Project"
            return
        if hasattr(self, '_config'):
            self._config(proj)


