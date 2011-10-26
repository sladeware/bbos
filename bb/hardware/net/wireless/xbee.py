#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Device

class XBee(Device):
    def __init__(self):
        Device.__init__(self, "XBee")
