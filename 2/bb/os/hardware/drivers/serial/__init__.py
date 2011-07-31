#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os import Command, BBOS_DRIVER_OPEN
from bb.os.hardware import Driver

class SERIAL_SEND_BYTE(Command):
    pass

class SERIAL_RECEIVE_BYTE(Command):
    pass

class serial(Driver):
    name='Serial',
    description='Standard serial driver',
    commands=[BBOS_DRIVER_OPEN, SERIAL_SEND_BYTE, SERIAL_RECEIVE_BYTE]

    def serial_open(self):
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
                self.serial_open()
            if message.get_command() is SERIAL_SEND_BYTE:
                self.serial_send_byte()
            elif message.get_command() is SERIAL_RECEIVE_BYTE:
                self.serial_receive_byte()
