#!/usr/bin/env python

from bb.eda.components.component import *

class Wire(Primitive):
    """A wire is an electrical design primitive. It is an object that
    forms an electrical connection between points on a schematic and is
    analogous to a physical wire."""

    def __init__(self):
        Primitive.__init__(self)

    def connect(self, first_pin, second_pin):
        self.first_pin = first_pin
        self.second_pin = second_pin

    def disconnect(self):
        self.first_pin = self.second_pin = None

    def get_first_pin(self):
        return self.first_pin
        
    def get_second_pin(self):
        return self.second_pin

class Bus(Primitive):
    """A bus is an electrical design primitive. It is an object that represents
    a multi-wire connection."""

