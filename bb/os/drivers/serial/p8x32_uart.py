#!/usr/bin/env python

__copyright__ = "Copyrigth (c) 2011 Sladeware LLC"

"""
P8X32 Uart driver.

Arguments:
    nr_devices     number of required devices
    mp_size        messaging pool size of uart driver
"""

import sys
import time
import types

from bb.os import get_running_kernel, get_running_thread, Message, printk
from bb.os import kernel
from bb.os.drivers.serial.core import Uart
from bb.mm.mempool import MemPool, mwrite
import serial

# Memory pools for various purposes
open_mp = None
write_mp = None

class Settings(object):
    def __init__(self, rx=None, tx=None, baudrate=115200,
                 simulation_port=None):
        self.rx = rx
        self.tx = tx
        self.baudrate = baudrate
        self.simulation_port = simulation_port

class SerialDevice(object):
    def __init__(self, settings=None):
        self.is_open = None
        self.owner = None
        self.settings = settings
        self.simulator = None

class P8X32Uart(Uart):
    """This class describes P8X32 uart driver."""
    name="P8X32_UART_DRIVER"
    # List of supported commands
    commands=('SERIAL_OPEN', 'SERIAL_CLOSE', 'SERIAL_WRITE', 'SERIAL_READ',
              'SERIAL_OPEN_FINALIZE')

    # Device table
    devices = []

    def p8x32_uart_open(self, message):
        """Open P8X32 serial device. This happens only when GPIO driver open
        appropriate pins for serial device."""
        device = message.get_data()
        self.devices.append(device)
        settings = device.settings
        #device.owner = message.get_sender()
        mask = (1 << settings.rx) + (1 << settings.tx)
        # Send open command to GPIO driver and wait for response
        gpio = get_running_kernel().find_module('bb.os.drivers.gpio.p8x32_gpio')
        if not gpio.open(mask):
            message.set_command('SERIAL_OPEN')
            get_running_kernel().send_message("P8X32_UART_DRIVER_PORT", message)
            return
        device.is_opened = True
        try:
            s = serial.Serial(port=settings.simulation_port,
                              baudrate=settings.baudrate)
            s.flushInput()
            s.flushOutput()
            device.simulator = s
        except serial.SerialException, e:
            sys.stderr.write("Could not open serial port: %s\n" % e)
            sys.exit(1)
        message.set_data(device)
        get_running_kernel().send_message(message.get_owner(), message)

    def p8x32_uart_read(self, message):
        device = message.get_data().device
        sim = device.simulator
        if not sim:
            return
        buf = sim.read(bytes)

    def p8x32_uart_write(self, message):
        device = message.get_data()[0]
        sim = device.simulator
        if not sim:
            get_running_kernel().send_message(message.get_sender(), message)
            return
        sim.write(message.get_data()[1])
        # there might be a small delay until the character is ready
        # (especially on win32)
        time.sleep(0.05)
        get_running_kernel().send_message(message.get_sender(), message)

    @Uart.runner
    def p8x32_uart(self):
        """Runner for this driver."""
        # Receive a new message. Return control to the next thread
        # if no messages.
        message = get_running_kernel().receive_message("P8X32_UART_DRIVER_PORT")
        if not message:
            return
        if message.get_command() == 'SERIAL_OPEN':
            self.p8x32_uart_open(message)
        elif message.get_command() == 'SERIAL_WRITE':
            self.p8x32_uart_write(message)

devices = MemPool(3, 1)

waiting = 0

def open(rx=None, tx=None, baudrate=115200, simulation_port=None):
    """Open uart driver. Return device instance."""
    global waiting
    if waiting & ((1 << rx) + (1 << tx)):
        port = get_running_kernel().select_port("P8X32_UART_INTERFACE_PORT")
        for i in range(port.get_num_messages()):
            message = port.touch_message(i)
            device = message.get_data()
            if device.settings.rx == rx and device.settings.tx == tx:
                message = port.get_message_by_index(i)
                get_running_kernel().free_message(message)
                return device
        return None
    # Select interface port and try to allocate a new message for communication
    message = get_running_kernel().alloc_message("P8X32_UART_INTERFACE_PORT",
                                                 "SERIAL_OPEN")
    if not message:
        printk("'%s' port does not have free messages." % port.get_name())
        return None
    # A new message was successfully allocated. Allocate a memory for
    # device structure.
    device = devices.malloc()
    if not device:
        printk("Not enough memory to allocate for device structure")
        port.free_message(message)
        return None
    settings = Settings(rx, tx, baudrate, simulation_port)
    device = SerialDevice(settings)
    device.owner = get_running_thread().get_name()
    message.set_data(device)
    get_running_kernel().send_message('P8X32_UART_DRIVER_PORT', message)
    waiting ^= (1 << rx) + (1 << tx)
    return None

def close(device):
    pass

def read(device, bytes=1):
    sim_serial = table[get_running_thread().get_name()]
    buf = sim_serial.read(bytes)
    return buf

def write(device, buf, sz=None):
    global write_mp
    message = get_running_kernel().touch_last_message("P8X32_UART_INTERFACE_PORT")
    if message and message.get_command() == "SERIAL_WRITE":
        message = get_running_kernel().receive_message("P8X32_UART_INTERFACE_PORT")
        write_mp.free(message.get_data())
        get_running_kernel().free_message(message)
    message = get_running_kernel().alloc_message("P8X32_UART_INTERFACE_PORT",
                                                 "SERIAL_WRITE")
    if not message:
        printk("No free memory for a message")
        return
    # Get some memory for a message data
    args = write_mp.malloc()
    if not args:
        get_running_kernel().free_message(message)
        printk("No free memory for message data2")
        return
    if not isinstance(buf, types.StringType):
        buf = str(buf)
    if not sz:
        # Data wasn't specify we will transfer all the data from buffer
        sz = len(buf)
    mwrite(args, [device, buf, sz])
    message.set_data(args)
    # Now try to send a message to driver
    get_running_kernel().send_message("P8X32_UART_DRIVER_PORT", message)

def bootstrap(args):
    # P8X32 serial gpio driver requires P8X32 GPIO driver for internal GPIO
    # manipulations.
    gpio = get_running_kernel().load_module('bb.os.drivers.gpio.p8x32_gpio')

    global open_mp, write_mp
    nr_devices = args.get('nr_devices', 1)
    mp_size = args.get('mp_size', 1)
    open_mp = MemPool(1, 1)
    write_mp = MemPool(1, 1)

    get_running_kernel().add_port("P8X32_UART_INTERFACE_PORT", 3)
    get_running_kernel().add_port("P8X32_UART_DRIVER_PORT", 1)

    driver = P8X32Uart()
    get_running_kernel().register_driver(driver)

import bb.os.drivers.serial.p8x32_uart.setup
