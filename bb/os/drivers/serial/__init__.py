#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os import get_running_kernel, Port, Driver, Messenger

class SerialMessenger(Messenger):
    PORT_NAME_FORMAT = "SERIAL_PORT_%d"

    @Messenger.message_handler("SERIAL_OPEN")
    def serial_open_handler(self, message):
        print "!"

    @Messenger.message_handler("SERIAL_CLOSE")
    def serial_close_handler(self, message):
        print "!"

class SerialDriver(Driver):
    MESSENGER_CLASS = SerialMessenger

    def init(self):
        pass

    def exit(self):
        pass
