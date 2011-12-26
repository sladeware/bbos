#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.eda import Primitive, Symbol

#_______________________________________________________________________________

class Part(Symbol):
    """A part is an electrical design primitive. It is a schematic symbol that
    represents an electronic device, such as a resistor, switch, operational
    amplifier, IC, etc."""

    def __init__(self):
        Symbol.__init__(self)
        self.__pins = dict()

    def add_pin(self, pin):
        if self.has_pin(pin):
            raise Exception("'%s' already has pin '%s'" \
                                % (self.metadata.name, pin.designator))
        self.__pins[pin.id] = pin

    def has_pin(self, pin):
        return pin.designator in self.__pins

    def find_pin(self, id_):
        return self.__pins.get(id_, None)

    def count_pins(self):
        return len(self.get_pins())

    def get_pins(self):
        return self.__pins.values()

#_______________________________________________________________________________


#_______________________________________________________________________________

class Component(object):
    """Each component can contain one or more parts."""
    
    def add_part(self):
        pass

