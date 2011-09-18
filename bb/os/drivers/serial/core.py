#!/usr/bin/evn python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

# Import PySerial for simulation purposes.
# Please, see http://pyserial.sourceforge.net/pyserial_api.html for more details
import serial

SERIAL_MODE_INVERT_RX      = 1
SERIAL_MODE_INVERT_TX      = 2
SERIAL_MODE_OPENDRAIN_TX   = 4
SERIAL_MODE_IGNORE_TX_ECHO = 8


from bb.os import Driver

class Uart(Driver):
    pass
