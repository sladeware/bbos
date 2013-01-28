#!/usr/bib/env python

import sys
import serial

try:
    sio = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
    sio.open()
    while True:
        c = sio.read()
        # print "'%s' {0:d} ==> {0:b}".format(ord(c), ord(c)) % c
        sys.stdout.flush()
        sys.stdout.write(c)
    sio.close()
except KeyboardInterrupt:
    pass
