#!/usr/bin/env python

"""Design blinker's process"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import time

from bb import os
from bb import app

LED=1
TIMEOUT=3

def blink_runner():
    print "Blink LED#%d!" % LED
    time.sleep(TIMEOUT) # in seconds

kernel = os.Kernel()
kernel.set_scheduler(os.StaticScheduler())
kernel.add_thread("BLINK", blink_runner)

if app.get_mode() is app.SIMULATION_MODE:
	kernel.start()	

