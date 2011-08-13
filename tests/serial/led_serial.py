#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import time

from bb.app import config, Mapping, Application
from bb.os import get_running_kernel, Kernel, StaticScheduler
from bb.os.hardware.boards import PropellerDemoBoard

def receiver():
    time.sleep(2)
    get_running_kernel().printer("Hi!")

def create_os_receiver():
    kernel = Kernel()
    kernel.set_scheduler(StaticScheduler())
    kernel.load_module('bb.os.drivers.serial.p8x32_uart')
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
        time.sleep(2)
        sender.init_complete = getattr(sender, 'init_complete', False)
        if not sender.init_complete:
            if uart.uart_open(dev):
                get_running_kernel().printer("Serial connection was established: %s" % dev_settings.simulation_port)
                sender.init_complete = True
            return

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
