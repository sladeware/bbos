#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""
Driver for XBee 802.15.4 radio modules with ZB or ZNet 2.5 firmware.

Please refer to Digi XBee product documentation for further details on frame
formats and AT commands:

  XBee Znet 2.5 modules product manual
    http://ftp1.digi.com/support/documentation/90000866_C.pdf

  XBee/XBee-PRO ZB OEM RF modules product manual
    http://ftp1.digi.com/support/documentation/90000976_a.pdf
"""

from bb.os import Driver, get_running_kernel

class XBeeDriver(Driver):
    NAME = "XBEE_DRIVER"

    # Carriage Return character
    CR = chr(13)

    def open(self, dev, serial_dev):
        pass

    def close(self):
        pass

    def tx(self, dev, array, sz=None):
        """Transmit an array of bytes array."""
        if not isinstance(array, bytearray):
            raise Exception("Not a bytearray type")

def on_load():
    get_running_kernel().register_driver(XBeeDriver)

def on_unload():
    pass
