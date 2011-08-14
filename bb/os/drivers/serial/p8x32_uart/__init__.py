#!/usr/bin/env python

__copyright__ = "Copyrigth (c) 2011 Sladeware LLC"

"""
Available modes:

  SERIAL_MODE_INVERT_RX -- invert rx
  SERIAL_MODE_INVERT_TX -- invert tx
  SERIAL_MODE_OPENDRAIN_TX -- pen-drain/source tx
  SERIAL_MODE_IGNORE_TX_ECHO -- ignore tx echo on rx
"""

import sys
import time
import types

from bb.os import get_running_kernel, get_running_thread, Message
from bb.os.drivers.serial.core import Uart
import serial

# P8X32 serial gpio driver requires P8X32 GPIO driver for internal GPIO
# manipulations. Similar to: `import p8x32_gpio as gpio'.
gpio = \
    get_running_kernel().load_module('bb.os.drivers.gpio.p8x32_gpio')

SERIAL_MODE_INVERT_RX      = 1
SERIAL_MODE_INVERT_TX      = 2
SERIAL_MODE_OPENDRAIN_TX   = 4
SERIAL_MODE_IGNORE_TX_ECHO = 8

table = {}

class Settings(object):
    def __init__(self, rx=None, tx=None, baudrate=115200,
                 simulation_port=None):
        self.rx = rx
        self.tx = tx
        self.baudrate = baudrate
        self.simulation_port = simulation_port

class SerialDevice(object):
    def __init__(self, settings=None):
        self.is_opened = False
        self.settings = settings

class P8X32Uart(Uart):
    """Class describes P8X32 Uart driver."""
    name="P8X32_UART"
    commands=('BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE')

    def p8x32_uart_open(self, message):
        device = message.get_data()
        settings = device.settings
        mask = sum([1 << getattr(settings, attr) for attr in 'rx', 'tx'])
        if gpio.gpio_open(mask):
            device.is_opened = True
            try:
                ser = serial.Serial(port=settings.simulation_port,
                                    baudrate=settings.baudrate)
                ser.flushInput()
                ser.flushOutput()
                table[message.get_sender()] = ser
            except serial.SerialException, e:
                sys.stderr.write("Could not open serial port: %s\n" % e)
                sys.exit(1)

    @Uart.runner
    def p8x32_uart(self):
        message = get_running_kernel().receive_message()
        if not message:
            return
        if message.get_command() is 'BBOS_DRIVER_OPEN':
            self.p8x32_uart_open(message)

def uart_open(device):
    if get_running_thread().get_name() in table:
        return True
    message = Message("BBOS_DRIVER_OPEN", device)
    get_running_kernel().send_message("P8X32_UART", message)
    return False

def uart_read(device, bytes=1):
    sim_serial = table[get_running_thread().get_name()]
    buf = sim_serial.read(bytes)
    return buf

def uart_write(device, data):
    sim_serial = table[get_running_thread().get_name()]
    if not isinstance(data, types.StringType):
        data = str(data)
    sim_serial.write(data)
    # there might be a small delay until the character is ready
    # (especially on win32)
    time.sleep(0.05)

get_running_kernel().register_driver(P8X32Uart())

import bb.os.drivers.serial.p8x32_uart.setup
