#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"
__version__ = "0.0.1"

from bb.os import get_running_kernel
from bb.os.drivers.serial import SerialDriver

class PropellerP8X32SerialDriver(SerialDriver):
    """A class representing a serial driver interface for Propeller P8X32
    microcontroller."""

    NAME = "PROPELLER_P8X32_SERIAL_DRIVER"

    # The following constants represent supported connection modes
    SERIAL_MODE_DEFAULT        = 0
    SERIAL_MODE_INVERT_RX      = 1
    SERIAL_MODE_INVERT_TX      = 2
    SERIAL_MODE_OPENDRAIN_TX   = 4
    SERIAL_MODE_IGNORE_TX_ECHO = 8

    def serial_open(self):
        """Called when the serial has to be open."""
        print 2

    def serial_close(self):
        pass

    def serial_read(self):
        pass

    def serial_write(self):
        pass

def on_load():
    # The driver requires a port for communication purposes
    get_running_kernel().register_driver(PropellerP8X32SerialDriver)

def on_unload():
    get_running_kernel().unregister_driver(PropellerP8X32SerialDriver)
