#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time

from bb import app
import bb.os as bbos
from bb.os.hardware.boards import PropellerDemoBoard
import sys

LED = 1
TIMEOUT = 3

def blink_runner():
    print "Blink LED#%d!" % LED
    time.sleep(TIMEOUT) # in seconds

kernel = bbos.Kernel()
kernel.set_scheduler(bbos.StaticScheduler())
kernel.add_thread("BLINK", blink_runner)

# Start to describe application and process it includes

blinker = app.Process('blinker', kernel)
board = PropellerDemoBoard(processes=[blinker])

blinker.run()

