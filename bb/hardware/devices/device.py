#!/usr/bin/env python

import networkx

from bb.hardware import primitives

class Sketch(object):
    G = networkx.Graph()

    def __init__(self):
        pass

class Device(primitives.ElectronicPrimitive):
    DRIVER_CLASS=None

    DESIGNATOR_FORMAT="D%d"

    def __init__(self, designator=None, designator_format=None):
        primitives.ElectronicPrimitive.__init__(self, designator,
                                                 designator_format)

    @property
    def G(self):
        return self._g

    def is_connected_to_element(self, element):
        return Sketch.G.has_edge(self, element)

    def add_elements(self, elements):
        for element in elements:
            self.add_element(element)

    def add_element(self, element):
        self.connect_to(element)
        return element

    def update_element(self, original, new):
        original_designator = original.get_designator()
        self.remove_element(original)
        new.set_designator(original_designator)
        self.add_element(new)

    def remove_element(self, element):
        pass

    def get_elements(self):
        return Sketch.G.neighbors(self)

    def find_element(self, by):
        pass

    def find_elements(self, by):
        return []

    def connect_to(self, element):
        Sketch.G.add_edge(self, element)

    def disconnect_elements(self, src, dest):
        pass

    def clone(self):
        """Clone this device instance."""
        clone = primitives.ElectronicPrimitive.clone(self)
        for origin_pin in self.find_elements(primitives.Pin):
            pin = origin_pin.clone()
            clone.add_element(pin)
        return clone

    def __str__(self):
        return "Device <%s>" % self.get_designator()
