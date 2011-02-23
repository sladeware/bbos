
import sys

__copyright__ = ""
__revision__ = ""

thread_name = "H48C"
thread_messages = ["H48C_FREE_FALL", "H48C_GFORCE_AOX", "H48C_GFORCE_AOY",
"H48C_GFORCE_AOZ"]

class H48C:
    def __init__(self, kernel):
        kernel.add_thread(thread_name)
        kernel.add_messages(thread_messages)
        
    def _config(self, proj):
        print "H48C Config"




