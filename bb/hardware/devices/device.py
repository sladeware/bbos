#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import types
import networkx

from bb.eda.primitives import *

class Device(ElectronicPrimitive):
    """This class represents a physical device. Device is any type of
    electrical component. It will have functions and properties unique
    to its type. Each device can contain one or more parts that are
    packaged together (e.g. a 74HCT32)."""

    # Device register keeps complete list of all devices so the instance
    # of device can not be managed by different device managers.
    element_register = dict()

    def __init__(self):
        ElectronicPrimitive.__init__(self)
        self.__g = networkx.Graph()

    def register_driver(self, driver):
        pass

    def unregister_driver(self, driver):
        pass

    def __get_default_driver(self):
        return None

    def add_element(self, element):
        if self.has_part(element):
            return element
        if id(element) in self.element_register:
            raise Exception("The element '%s' already belongs to '%s'" \
                                % (element, self.element_register[id(element)]))
        # Assume designator
        if element.designator:
            if self.find_element(element.designator):
                pass
        else:
            if not element.designator_format:
                raise Exception("Element %s does not have designator format." \
                                    % element)
            relatives = self.find_elements(self.__class__)
            element.designator = element.designator_format % len(relatives)
        self.element_register[id(element)] = self
        self.__g.add_node(element)
        return element

    def update_element(self, original, new):
        """The `original` element is replacing by a `new`, whose
        designator attribute is set to the designator of the original
        element."""
        original_designator = original.designator()
        self.remove_element(original)
        new.designator(original_designator)
        self.add_element(new)

    def remove_element(self, element):
        self.__g.remove_node(element)
        del Device.element_register[id(element)]

    def get_elements(self):
        """Return list of elements that belongs to this device."""
        return self.__g.nodes()

    def find_element(self, by):
        """If there is more than one child matching the search, the first
        one is returned. In that case, Device.find_elements() should be used."""
        elements = self.find_elements(by)
        return elements.pop(0)

    def find_elements(self, by):
        """Returns elements of this device that is identified by `by`,
        or None if there is no such object.

        The by argument can be represented by a function, string, class or
        number. Omitting the by argument causes all object to be matched."""
        elements = list()
        if type(by) == types.TypeType:
            for element in self.get_elements():
                if isinstance(element, by):
                    elements.append(element)
        return elements

    def has_element(self, element):
        return element in self.__elements

    def connect_elements(self, dest, src=None):
        if not src:
            src = self
        for part in (src, dest):
            self.add_element(element)
        self.__g.add_edge(src, dest)

    def disconnect_parts(self, src, dest):
        pass
