#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

from bb.hardware.devices import Device

class LED(Device):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

    def __init__(self, color=None):
        Device.__init__(self)
        self.__color = color

    def get_color(self):
        return self.__color

    def __str__(self):
        return "LED <%s> [color=%s]" % (self.get_designator(), self.get_color())
