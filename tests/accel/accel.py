#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time

from bb import app
from bb.os import get_running_kernel, Kernel, StaticScheduler
from bb.os.hardware.boards import PropellerDemoBoard

kernel = Kernel()
kernel.set_scheduler(StaticScheduler())
h48c = kernel.load_module('bb.os.hardware.drivers.accel.h48c')

device_settings = h48c.H48CDeviceSettings(7, 6, 0, 1)
device = h48c.AccelDevice(settings=device_settings)

def freefall_runner():
    time.sleep(1) # So we humans can see output
    freefall_runner.init_complete = getattr(freefall_runner, 'init_complete', False)
    if not freefall_runner.init_complete:
        if h48c.accel_open(device):
            get_running_kernel().printer("Accelerometer device has been opened")
            freefall_runner.init_complete = True
        return
    if h48c.accel_freefall():
        get_running_kernel().printer("Free fall detected!")
    else:
        get_running_kernel().printer("No free fall")

kernel.add_thread('FREEFALL', freefall_runner)
accel = app.Process("Accel", kernel)
board = PropellerDemoBoard(processes=[accel])

accel.run()

