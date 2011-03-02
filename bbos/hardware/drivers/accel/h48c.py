
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.module import Module

thread_name = "H48C"
thread_messages = ["H48C_FREE_FALL", "H48C_GFORCE_AOX", "H48C_GFORCE_AOY",
"H48C_GFORCE_AOZ"]

class H48C(Module):
    def __init__(self, kernel):
        Module.__init__(self, "H48C Accelerometer Driver")
        kernel.add_thread(thread_name)
        kernel.add_messages(thread_messages)





