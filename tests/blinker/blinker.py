#!/usr/bin/env python

"""Design blinker's application"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

# Start to describe operating system's kernel
import time

from bb import os

LED = 1
TIMEOUT = 3

def blink_runner():
    print "Blink LED#%d!" % LED
    time.sleep(TIMEOUT) # in seconds

kernel = os.Kernel()
kernel.set_scheduler(os.StaticScheduler())
kernel.add_thread("BLINK", blink_runner)

# Start to describe application and process it includes
from bb import app
from bb.os.hardware.boards import PropellerDemoBoard

blinker = app.Process('blinker', kernel)
board = PropellerDemoBoard([blinker])

if app.get_mode() is app.SIMULATION_MODE:
	blinker.run()

