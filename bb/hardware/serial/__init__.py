#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Device

class SerialDevice(Device):
    NAME_FORMAT = "SERIAL_DEVICE_%d"
    
    def __str__(self):
        return "Serial device '%s'" % self.get_name()
