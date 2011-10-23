#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"
__version__ = "0.0.1"

from bb.os import get_running_kernel, Port
#from bb.os.drivers.serial import SerialDriver, SerialMessenger, IOSerialInterface

class PropellerP8X32SerialDriver():
    """A class representing a serial driver interface for P8X32
    microcontroller."""
    name="PROPELLER_P8X32_SERIAL_DRIVER"
    # The following constants represent supported connection modes
    SERIAL_MODE_DEFAULT        = 0
    SERIAL_MODE_INVERT_RX      = 1
    SERIAL_MODE_INVERT_TX      = 2
    SERIAL_MODE_OPENDRAIN_TX   = 4
    SERIAL_MODE_IGNORE_TX_ECHO = 8

    # The following methods implement common serial API that user will use to
    # handle serial device.

    def serial_open(self):
        """Called when the serial has to be open."""
        pass

    def serial_close(self):
        pass

    def serial_read(self):
        pass

    def serial_write(self):
        pass

def on_load():
    # The driver requires a port for communication purposes
    get_running_kernel().add_port(Port(P8X32SerialMessenger.port_name, 3))
    _driver = P8X32SerialDriver()
    get_running_kernel().register_driver(_driver)

def on_unload():
    get_running_kernel().unregister_driver(_driver)
    get_running_kernel().remove_port_by_name("P8X32SERIAL_P0")
