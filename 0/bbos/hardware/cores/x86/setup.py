"""No frills single x86 core.
"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.hardware.core import *

class x86(Core):
    def __init__(self, process):
        Core.__init__(self, "x86", process)



