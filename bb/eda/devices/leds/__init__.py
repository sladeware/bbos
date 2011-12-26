#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Part

class LED(Part):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"

    def __init__(self, color=None):
        Part.__init__(self, "LED")
        self.__color = color

    def get_color(self):
        return self.__color

    def __str__(self):
        return "LED [color=%s]" % (self.get_color(),)
