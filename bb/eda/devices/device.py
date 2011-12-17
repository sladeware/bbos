#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import types
import networkx

from bb.eda.primitives import *

#_______________________________________________________________________________

class Wire(Primitive):
    """A wire is an electrical design primitive. It is a polyline object that
    forms an electrical connection between points on a schematic and is
    analogous to a physical wire."""

class Device(Symbol, Distributable):
    """This class represents a physical device that is placed on the
    board, e.g. the integrated circuit or resistor. Each device can
    contain one or more parts that are packaged together (e.g. a
    74HCT32)."""

    # Device register keeps complete list of all devices so the instance
    # of device can not be managed by different device managers.
    part_register = dict()

    def __init__(self):
        Symbol.__init__(self)
        Distributable.__init__(self)
        self.__g = networkx.Graph()
 
    def set_driver(self, driver):
        self._driver = driver

    def get_driver(self):
        if not self._driver:
            self._driver = self.__get_default_driver()
        return self._driver

    def __get_default_driver(self):
        return None

    def add_part(self, part):
        if self.has_part(part):
            return part
        if id(part) in self.part_register:
            raise Exception("The part '%s' already belongs to '%s'" \
                                % (part, self.part_register[id(part)]))
        # Assume designator
        if part.designator:
            if self.find_part(part):
                pass
        else:
            if not part.designator_format:
                raise Exception("Part %s does not have designator format." \
                                    % part)
            relatives = self.find_parts(by=self.__class__)
            part.designator = part.designator_format % len(relatives)
        self.part_register[id(part)] = self
        self.__g.add_node(part)
        return part

    def replace_part(self, original, target):
        """The original part is replacing by a target device, whose
        designator attribute is set to the designator of the original part."""
        original_designator = original.designator()
        self.remove_part(original)
        target.designator(original_designator)
        self.add_part(target)

    def remove_part(self, part):
        self.__g.remove_node(part)
        del Component.part_register[id(part)]

    def get_parts(self):
        """Return list of devices that belong to this device manager."""
        return self.__g.nodes()

    def find_part(self, by):
        """If there is more than one child matching the search, the first
        one is returned. In that case, Part.find_parts() should be used."""
        parts = self.find_parts(by)
        return parts.pop(0)

    def find_parts(self, by):
        """Returns parts of this component that is identified by by,
        or None if there is no such object.

        The by argument can be represented by a function, string, class or
        number. Omitting the by argument causes all object to be matched."""
        parts = list()
        if type(by) == types.TypeType:
            for part in self.get_parts():
                if isinstance(part, by):
                    parts.append(part)
        return parts

    def has_part(self, part):
        return self.__g.has_node(part)

    def connect_parts(self, dest, src=None):
        if not src:
            src = self
        for part in (src, dest):
            self.add_component(part)
        self.__g.add_edge(src, dest)

    def disconnect_parts(self, src, dest):
        pass
