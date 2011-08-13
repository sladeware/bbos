#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import random

from bb.os import get_running_kernel, Driver, Message

gpio = get_running_kernel().load_module('bb.os.drivers.gpio.p8x32_gpio')

class H48CDeviceSettings(object):
    def __init__(self, dio_pin=None, clk_pin=None, cs_pin=None, zerog_pin=None):
        self.dio_pin = dio_pin
        self.clk_pin = clk_pin
        self.cs_pin = cs_pin
        self.zerog_pin = zerog_pin

class AccelDevice(object):
    def __init__(self, settings=None):
        self.is_opened = False
        self.settings = settings

def accel_open(device):
    if device.is_opened:
        # Device was already opened return True value
        return True
    # Device was not opened. Send a message with BBOS_DRIVER_OPEN command
    # to the H48CDriver.
    get_running_kernel().send_message('H48C', Message('BBOS_DRIVER_OPEN', device))
    return False

def accel_freefall():
    return int(random.random() + 0.1)

class H48CDriver(Driver):
    name='H48C'
    description='H48C Accelerometer Driver'
    commands=('BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE')

    def h48c_open(self, device):
        mask = sum([1 << getattr(device.settings, attr) for attr in 'dio_pin',
                    'clk_pin', 'cs_pin', 'zerog_pin'])
        if gpio.gpio_open(mask):
            device.is_opened = True

    @Driver.runner
    def h48c_runner(self):
        message = self.get_message()
        if message:
            if message.get_command() == 'BBOS_DRIVER_OPEN':
                self.h48c_open(message.get_data())
            get_running_kernel().send_message(message.get_sender(), message)

get_running_kernel().register_driver(H48CDriver())

import bb.os.drivers.accel.h48c.setup
