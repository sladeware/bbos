#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import types

from bb.hardware.primitives import *

class Device(ElectronicPrimitive):
    """This class is sub-class of
    :class:`bb.hardware.primitives.ElectronicPrimitive` and represents a
    physical device. Device is any type of electrical component. It
    will have functions and properties unique to its type. Each device
    can contain one or more parts that are packaged together (e.g. a
    74HCT32)."""

    class Searcher(list):
        def __init__(self, source):
            self.__source = source
            self.__elements = []
            list.__init__(self, self.__source)

        def find_elements(self, by):
            """Returns elements of this device that is identified by `by`,
            or ``None`` if there is no such object.

            The by argument can be represented by a function, string, class or
            number. Omitting the by argument causes all object to be matched."""
            if type(by) == types.TypeType:
                for element in self.__source:
                    if isinstance(element, by):
                        self.__elements.append(element)
            elif type(by) in (types.StringType, types.UnicodeType):
                for element in self.__source:
                    if element.designator == by:
                        self.__elements.append(element)
            return Device.Searcher(self.__elements)

        def find_element(self, by):
            """If there is more than one child matching the search, the first
            one is returned. In that case, :func:`Device.find_elements` should
            be used."""
            elements = self.find_elements(by)
            if len(elements):
                return elements[0]
            return None

    # Device register keeps complete list of all devices so the instance
    # of device can not be managed by different device managers.
    element_register = dict()

    def __init__(self):
        ElectronicPrimitive.__init__(self)

    def register_driver(self, driver):
        pass

    def unregister_driver(self, driver):
        pass

    def __get_default_driver(self):
        return None

    def has_element(self, element):
        global G
        return G.has_edge(self, element)

    def add_element(self, element):
        """Add `element` to device.

        Note, the element instance can only belong to one device instance.
        Otherwise you will get an exception."""
        #if self.has_element(element):
        #    return element
        #if id(element) in Device.element_register:
        #    raise Exception("The element '%s' already belongs to '%s'" \
        #                        % (element, Device.element_register[id(element)]))
        #Device.element_register[id(element)] = self
        # Assume designator
        if element.get_property_value("name"):
            if self.find_element(element.designator):
                pass
        else:
            if not element.designator_format:
                raise Exception("Element %s does not have designator format." \
                                    % element)
            relatives = self.find_elements(self.__class__)
            element.designator = element.designator_format % len(relatives)
        self.connect_to(element)
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
        """Remove element from this device."""
        #G.remove_node(element)
        #del Device.element_register[id(element)]
        pass

    def get_elements(self):
        """Return list of elements that owns to this device."""
        global G
        return G.neighbors(self)

    def find_element(self, by):
        """If there is more than one child matching the search, the first
        one is returned. In that case, Device.find_elements() should be used."""
        elements = self.find_elements(by)
        if len(elements):
            return elements[0]
        return None

    def find_elements(self, by):
        """Returns elements of this device that is identified by `by`,
        or None if there is no such object.

        The by argument can be represented by a function, string, class or
        number. Omitting the by argument causes all object to be matched."""
        searcher = Device.Searcher(self.get_elements())
        return searcher.find_elements(by)

    def connect_to(self, element):
        """Connect two elements."""
        #print self.get_property_value("name"), element.designator
        global G
        G.add_edge(self, element)

    def disconnect_elements(self, src, dest):
        pass

    def clone(self):
        clone = ElectronicPrimitive.clone(self)
        for origin_pin in self.find_elements(Pin):
            pin = origin_pin.clone()
            clone.add_element(pin)
        return clone

def verify_device(device):
    pass
