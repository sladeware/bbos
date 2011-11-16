#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Device

#_______________________________________________________________________________

class XBee(Device):
    NAME_FORMAT = "XBEE_%d"

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object."""
        return "Xbee 802.15.4 radio module"
