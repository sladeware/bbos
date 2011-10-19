#!/usr/bin/env python

"""
IOP8X32SerialMessenger is subclass of IOSerialMessenger which is a subclass of
IOMessenger.
"""

__version__ = "0.0.1"

from bb.os.kernel import get_running_kernel, Port
from bb.os.drivers.serial import SerialDriver, SerialMessenger, IOSerialInterface

class P8X32SerialMessenger(SerialMessenger):
    """This class represents a Messenger for P8X32 serial driver."""
    name="P8X32SERIAL_MSNGR"
    port_name="P8X32SERIAL_PORT"

class IOP8X32SerialInterface(IOSerialInterface):
    """A class representing a serial interface for P8X32 microcontroller."""
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

class P8X32SerialDriver(SerialDriver):
    name="P8X32SERIAL"
    messenger_class=P8X32SerialMessenger
    iointerface_class=IOP8X32SerialInterface

# Make sure that a future driver instance is a private variable
_driver = None

def on_load(*args):
    """Load serial driver."""
    # The driver requires a port for communication purposes
    get_running_kernel().add_port(Port(P8X32SerialMessenger.port_name, 3))
    _driver = P8X32SerialDriver()
    get_running_kernel().register_driver(_driver)

def on_unload(*args):
    """Unload serial driver."""
    get_running_kernel().unregister_driver(_driver)
    get_running_kernel().remove_port_by_name("P8X32SERIAL_P0")
    _driver = None
