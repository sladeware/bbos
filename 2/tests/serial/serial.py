#!/usr/bin/env python

#import bb.os as bbos

#kernel = bbos.Kernel()
#kernel.add_module('bb.os.hardware.drivers.serial')

import bb
import serial
import sys

s = serial.Serial()
s.port = '/dev/ttySL0'
s.baudrate = 115200

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("Could not open serial port %s: %s\n" % (s.portstr, e))
    sys.exit(1)

s.write("hello how are you")

