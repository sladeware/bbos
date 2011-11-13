#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Part

class XBee(Part):
    NAME_FORMAT = "XBEE_%d"

    def __str__(self):
        return "Xbee 802.15.4 radio module"
