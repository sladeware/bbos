#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import bb.os as bbos
from bb.os import Message, Command, BBOS_DRIVER_OPEN, Module
from bb.os.hardware import Driver
import bb.os.hardware.drivers.gpio as gpio

"""Available modes:
  SERIAL_MODE_INVERT_RX -- invert rx
  SERIAL_MODE_INVERT_TX -- invert tx
  SERIAL_MODE_OPENDRAIN_TX -- pen-drain/source tx
  SERIAL_MODE_IGNORE_TX_ECHO -- ignore tx echo on rx"""
SERIAL_MODE_INVERT_RX      = 1
SERIAL_MODE_INVERT_TX      = 2
SERIAL_MODE_OPENDRAIN_TX   = 4
SERIAL_MODE_IGNORE_TX_ECHO = 8

class SERIAL_SEND_BYTE(Command):
    pass

class SERIAL_RECEIVE_BYTE(Command):
    pass

class SerialSettings(object):
    """The structure to keep required serial settings."""
    def __init__(self, rx_pin, tx_pin, mode, baudrate):
        self.rx_pin = rx_pin
        self.tx_pin = tx_pin
        self.mode = mode
        self.baudrate = baudrate

def serial_open(settings):
    """Open a new serial connection by specified settings."""
    if not isinstance(settings, SerialSettings):
        raise Exception("serial settings my be defined by using SerialSettings")
    if not gpio.get_pins_owner(settings.rx_pin) and not gpio.get_pins_owner(settings.tx_pin):
        bbos.get_running_kernel().send_message("SERIAL", Message("DEMO", BBOS_DRIVER_OPEN, settings))

def serial_read(device, nbytes):
    pass

class serial(Module, Driver):
    name="SERIAL"
    description="Standard serial driver"
    commands=[BBOS_DRIVER_OPEN, SERIAL_SEND_BYTE, SERIAL_RECEIVE_BYTE]
    dependencies=[gpio]

    def serial_open(self, data):
        pass

    def serial_send_byte(self):
        pass

    def serial_receive_byte(self):
        pass

    @Driver.runner
    def serial_runner(self):
        message = self.get_message()
        if message:
            if message.get_command() is BBOS_DRIVER_OPEN:
                pass
            if message.get_command() is SERIAL_SEND_BYTE:
                self.serial_send_byte()
            elif message.get_command() is SERIAL_RECEIVE_BYTE:
                self.serial_receive_byte()

