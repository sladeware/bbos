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

class Pin(Symbol):
    """A pin is an electrical design primitive. Pins give a part its
    electrical properties and define connection points on the part for
    directing signals in and out."""

    class ElectricalTypes:
        """Class of possible electrical types."""
        Input = 0
        IO = 1
        Output = 2

    def __init__(self):
        Symbol.__init__(self)
        self._connections = dict()
        self.__electrical_type = None

    @property
    def electrical_type(self):
        """Electrical type represents the type of electrical connection the pin
        makes. This can be used to detect electrical wiring errors in your
        schematic."""
        return self.__electrical_type

    @electrical_type.setter
    def electrical_type(self, type_):
        if not getattr(Pin.ElectricalTypes, type_):
            raise
        self.__electrical_type = type_

    def connect_to(self, pin):
        """Connect source pin to destination pin."""
        if not self.is_connected_to(pin):
            self._connections[id(pin)] = pin
            pin.connect_to(self)

    def is_connected_to(self, pin):
        return id(pin) in self._connections

#_______________________________________________________________________________

class Component(object):
    """Each component can contain one or more parts."""
    
    def add_part(self):
        pass

