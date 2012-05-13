#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.hardware.devices import Device
from bb.os.drivers.net.wireless.xbee import XBeeDriver

class XBee(Device):
    DEFAULT_DRIVER_CLASS=XBeeDriver
    DEFAULT_DESIGNATOR_FORMAT="XBEE_%d"
    DEFAULT_SHORT_DESCRIPTION="Xbee 802.15.4 radio module"

