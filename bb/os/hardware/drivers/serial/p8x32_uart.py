
__copyright__ = "Copyrigth (c) 2011 Sladeware LLC"

"""
Available modes:

  SERIAL_MODE_INVERT_RX -- invert rx
  SERIAL_MODE_INVERT_TX -- invert tx
  SERIAL_MODE_OPENDRAIN_TX -- pen-drain/source tx
  SERIAL_MODE_IGNORE_TX_ECHO -- ignore tx echo on rx
"""

import sys

# Import PySerial for simulation purposes
import serial

from bb.os.kernel import get_running_kernel, get_running_thread, Driver, Message

# P8X32 serial gpio driver requires P8X32 GPIO driver for internal GPIO
# manipulations. Similar to: `import p8x32_gpio as gpio'.
gpio = get_running_kernel().load_module('bb.os.hardware.drivers.gpio.p8x32_gpio')

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

class P8X32Uart(Driver):
    name="P8X32_UART"
    commands=('BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE')

    def p8x32_uart_open(self, message):
        device = message.get_data()
        settings = device.settings
        mask = sum([1 << getattr(settings, attr) for attr in 'rx', 'tx'])
        if gpio.gpio_open(mask):
            device.is_opened = True
            try:
                table[message.get_sender()] = serial.Serial(
                    port=settings.simulation_port,
                    baudrate=settings.baudrate)
            except serial.SerialException, e:
                sys.stderr.write("Could not open serial port: %s\n" % e)
                sys.exit(1)

    @Driver.runner
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

def uart_read():
    pass

def uart_write(device, data):
    sim_serial = table[get_running_thread().get_name()]
    sim_serial.write(data)

get_running_kernel().register_driver(P8X32Uart())
