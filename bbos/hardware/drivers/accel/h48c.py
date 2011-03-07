
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.thread import Thread
from bbos.kernel.module import Module

class H48C(Module):
    def __init__(self, kernel):
        Module.__init__(self, "H48C Accelerometer Driver")
        self.thread = Thread("H48C", "h48c")
        # Introduce module to the kernel
        kernel.add_thread( self.get_thread() )
        kernel.add_messages( self.get_messages() )

    def get_thread(self):
        return self.thread

    def get_messages(self):
        return ["H48C_FREE_FALL", "H48C_GFORCE_AOX", 
                "H48C_GFORCE_AOY", "H48C_GFORCE_AOZ"]



