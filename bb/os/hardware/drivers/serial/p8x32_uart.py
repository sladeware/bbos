
__copyright__ = "Copyrigth (c) 2011 Sladeware LLC"

"""
Available modes:

  SERIAL_MODE_INVERT_RX -- invert rx
  SERIAL_MODE_INVERT_TX -- invert tx
  SERIAL_MODE_OPENDRAIN_TX -- pen-drain/source tx
  SERIAL_MODE_IGNORE_TX_ECHO -- ignore tx echo on rx
"""

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
    def __init__(self, rx=None, tx=None, 
                 simulation_port=None):
        self.rx = rx
        self.tx = tx
        self.simulation_port = simulation_port

class P8X32Uart(Driver):
    name="P8X32_UART"

    def p8x32_uart_open(self, message):
        table[message.get_sender()] = None

    @Driver.runner
    def p8x32_uart(self):
        message = get_running_kernel().receive_message()
        if not message:
            return
        if message.get_command() is 'BBOS_DRIVER_OPEN':
            self.p8x32_uart_open(message)

def uart_open(settings):
    if not get_running_thread().get_name() in table:
        message = Message("BBOS_DRIVER_OPEN", settings)
        get_running_kernel().send_message("P8X32_UART", message)

def uart_read():
    pass

def uart_write():
    pass

# Register driver 
get_running_kernel().add_driver(P8X32Uart())
