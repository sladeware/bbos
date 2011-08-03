#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time
import re

from bb.os.kernel import get_running_kernel, Kernel
from bb.os.kernel.schedulers import StaticScheduler

kernel = Kernel()
kernel.set_scheduler(StaticScheduler())
uart = kernel.load_module('bb.os.hardware.drivers.serial.p8x32_uart')

message = "Hello world!\n"

settings = uart.Settings(rx=0, tx=1, baudrate=115200, simulation_port='/dev/ttySL0')
device = uart.SerialDevice(settings)

def demo():
    time.sleep(1)
    demo.init_complete = getattr(demo, 'init_complete', False)
    if not demo.init_complete:
        if uart.uart_open(device):
            get_running_kernel().printer("Serial connection was established: %s" % settings.simulation_port)
            demo.init_complete = True
        return
    get_running_kernel().printer("Write to serial: '%s'" % message)
    uart.uart_write(device, message)

kernel.add_thread("DEMO", demo)
kernel.start()
