#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time

import bb
import bb.os as bbos
from bb.os.kernel.schedulers import StaticScheduler
import bb.os.hardware.drivers.serial as serial

demo_serial_settings = serial.SerialSettings(2, 3, serial.SERIAL_MODE_IGNORE_TX_ECHO, 1152200)

def demo():
    serial.serial_open(demo_serial_settings)
    time.sleep(2)

kernel = bbos.Kernel()
kernel.set_scheduler(StaticScheduler())
kernel.add_module(serial)
kernel.add_thread("DEMO", demo)

kernel.start()

"""
s = serial.Serial()
s.port = '/dev/ttySL0'
s.baudrate = 115200

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("Could not open serial port %s: %s\n" % (s.portstr, e))
    sys.exit(1)

s.write("hello how are you")

"""
