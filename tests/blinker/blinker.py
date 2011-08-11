#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time

from bb.app import Mapping, config
from bb.os import get_running_kernel, Kernel, StaticScheduler
from bb.os.hardware.boards import PropellerDemoBoard

LED = 1
TIMEOUT = 3 # in seconds

def blink_runner():
    get_running_kernel().printer("Blink LED#%d!" % LED)
    time.sleep(TIMEOUT)

def create_blinker():
    kernel = Kernel()
    kernel.set_scheduler(StaticScheduler())
    kernel.add_thread("BLINK", blink_runner)
    blinker = Mapping('blinker', kernel)
    board = PropellerDemoBoard(processes=[blinker])
    return blinker

if __name__=='__main__':
    config.parse_command_line()
    blinker = create_blinker()
    blinker.run()
