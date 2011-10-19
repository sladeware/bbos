#!/usr/bin/env python

from bb.os.kernel import Messenger, Driver, IOInterface

class SerialDriver(Driver):
    pass

class IOSerialInterface(IOInterface):
    pass

class SerialManager(object):
    def serial_register(self, message):
        print "!"

    def serial_unregister(self, message):
        print "!"

class SerialMessenger(Messenger):
    command_handlers_table=dict(
        SERIAL_REGISTER   = SerialManager.serial_register,
        SERIAL_UNREGISTER = SerialManager.serial_unregister
        )
