
import time

import sys

#print sys.path
#exit()

from bb.os.kernel import Kernel, Thread
from bb.os.kernel.schedulers import StaticScheduler

LED=1

def blink_runner():
    print "Blink LED#%d!" % LED
    time.sleep(3) # sleep for 3 seconds

blinker = Kernel()
blinker.set_scheduler(StaticScheduler())
blinker.add_thread("BLINK", blink_runner)

blinker.start()


