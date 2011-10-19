#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""A set of tools to interact with a hardware device."""

from bb.os import OSObject, OSObjectMetadata

class Device(OSObject):
    driver=None

    def __init__(self, driver=None):
        if driver:
            self.driver = driver

class Driver(OSObject, OSObjectMetadata):
    messenger_class=None
    iointerface_class=None

    def __init__(self, name=None, version=None):
        OSObjectMetadata.__init__(self, name)
        if version:
            self.version = version
        #self.__iointerface = self.iointerface_class()
        #self.__messenger = self.messenger_class()

    def get_version(self):
        return self.version

    def get_messenger(self):
        return self.__messenger

    def get_iointerface(self):
        return self.__iointerface

    def init(self):
        """Called by the system after driver registration."""
        pass

    def exit(self):
        """Called by the system once the driver was unregistered."""
        pass
