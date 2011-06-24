#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import time
import sys

from bb.os.kernel import Kernel, Thread
from bb.os.kernel.schedulers import StaticScheduler

LED=1
TIMEOUT=3

def blink_runner():
    print "Blink LED#%d!" % LED
    time.sleep(TIMEOUT) # in seconds

blinker = Kernel()
blinker.set_scheduler(StaticScheduler())
blinker.add_thread("BLINK", blink_runner)

