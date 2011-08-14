#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time
import random

from bb.app import config, Mapping, Application
from bb.os import get_running_kernel, Kernel, StaticScheduler
from bb.os.hardware.boards import PropellerDemoBoard

def create_os_receiver():
    kernel = Kernel()
    kernel.set_scheduler(StaticScheduler())
    uart = kernel.load_module('bb.os.drivers.serial.p8x32_uart')
    dev_settings = uart.Settings(rx=30, tx=31, baudrate=115200,
                                 simulation_port='/dev/ttySL0')
    dev = uart.SerialDevice(dev_settings)

    def receiver():
        time.sleep(1)
        receiver.init_complete = getattr(receiver, 'init_complete', False)
        if not receiver.init_complete:
            if uart.uart_open(dev):
                get_running_kernel().printer("Serial connection was "
                                             "established: %s" % dev_settings.simulation_port)
                receiver.init_complete = True
            return
        data = uart.uart_read(dev, 1)
        get_running_kernel().printer("Read from serial: %d'" % ord(data))
        get_running_kernel().printer("Blink LED #%d" % ord(data))

    kernel.add_thread("RECEIVER", receiver)
    return kernel

def create_sender():
    kernel = Kernel()
    kernel.set_scheduler(StaticScheduler())
    uart = kernel.load_module('bb.os.drivers.serial.p8x32_uart')
    dev_settings = uart.Settings(rx=0, tx=1, baudrate=115200,
                                 simulation_port='/dev/ttySL0')
    dev = uart.SerialDevice(dev_settings)

    def sender():
        time.sleep(1)
        sender.init_complete = getattr(sender, 'init_complete', False)
        if not sender.init_complete:
            if uart.uart_open(dev):
                get_running_kernel().printer("Serial connection was established: %s" % dev_settings.simulation_port)
                sender.init_complete = True
            return
        led = int(16 + random.random() * 8)
        get_running_kernel().printer("Write to serial: '%d'" % led)
        uart.uart_write(dev, chr(led))

    kernel.add_thread("SENDER", sender)
    return kernel

def application():
    receiver = Mapping(create_os_receiver())
    sender = Mapping(create_sender())
    board = PropellerDemoBoard(processes=[receiver])
    return Application(processes=[receiver, sender])

if __name__ == '__main__':
    config.parse_command_line()
    application().start()
