#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

import types

from bb.hardware import primitives

class Device(primitives.ElectronicPrimitive):
    """This class is sub-class of
    :class:`bb.hardware.primitives.ElectronicPrimitive` and represents a
    physical device. Device is any type of electrical component. It
    will have functions and properties unique to its type. Each device
    can contain one or more parts that are packaged together (e.g. a
    74HCT32).
    
    When the device is used under operating system, it manages it with help of
    :class:`bb.os.kernel.DeviceManager` and controles it with help of
    :class:`bb.os.kernel.Driver`. It is always better to define driver that will
    control your device when your are planing to create a device. When the
    driver is defined the operating system will use :func:`get_driver` method to
    obtaine driver instance and then use
    :func:`bb.os.kernel.HardwareManagement.bind_device_to_driver` in order to
    tie these two objects.
    """

    DRIVER_CLASS=None
    """This constant keeps default :class:`bb.os.kernel.Driver` class that
    can be taken by :func:`Device.get_driver`.
    """

    DESIGNATOR_FORMAT="D%d"

    class Searcher(list):
        def __init__(self, source):
            self.__source = source
            self.__elements = []
            list.__init__(self, self.__source)

        def find_elements(self, by):
            """Returns elements of this device that is identified by `by`,
            or ``None`` if there is no such object.

            The by argument can be represented by a function, string, class or
            number. Omitting the by argument causes all object to be matched.
            """
            if type(by) == types.TypeType:
                for element in self.__source:
                    if isinstance(element, by):
                        self.__elements.append(element)
            elif type(by) in (types.StringType, types.UnicodeType):
                for element in self.__source:
                    if element.get_designator() == by:
                        self.__elements.append(element)
            return Device.Searcher(self.__elements)

        def find_element(self, by):
            """If there is more than one child matching the search, the first
            one is returned. In that case, :func:`Device.find_elements` should
            be used.
            """
            elements = self.find_elements(by)
            if len(elements):
                return elements[0]
            return None

    # Device register keeps complete list of all devices so the instance
    # of device can not be managed by different device managers.
    element_register = dict()

    def __init__(self):
        primitives.ElectronicPrimitive.__init__(self)

    @property
    def G(self):
        """Return graph `G` that represents a structure of this device. All
        the device elements will be nodes of this graph.
        """
        return primitives.G

    def register_driver(self, driver):
        pass

    def unregister_driver(self, driver):
        pass

    def get_driver(self, version=None):
        """Return :class:`bb.os.kernel.Driver` class that will be used as driver
        to control this device. By default returns :const:`DRIVER_CLASS`."""
        return self.DRIVER_CLASS

    def is_connected_to_element(self, element):
        """Return whether or not the device is **directly** connected to 
        `element`.
        """
        return self.G.has_edge(self, element)

    def add_element(self, element):
        """Add `element` to device.

        .. note::

          An element instance can only belong to one device instance.
          Otherwise you will get an exception.
        """
        #if self.has_element(element):
        #    return element
        #if id(element) in Device.element_register:
        #    raise Exception("The element '%s' already belongs to '%s'" \
        #                        % (element, Device.element_register[id(element)]))
        #Device.element_register[id(element)] = self
        # Assume designator
        if element.get_property_value("name"):
            if self.find_element(element.get_designator()):
                pass
            # raise Exception("!")
        else:
            if not element.get_designator_format():
                raise Exception("Element %s does not have designator format." \
                                    % element)
            relatives = self.find_elements(self.__class__)
            element.generate_designator(counter=len(relatives))
        self.connect_to(element)
        return element

    def update_element(self, original, new):
        """The `original` element is replacing by a `new`, whose
        designator is set to the designator of the `original`
        element.
        """
        original_designator = original.get_designator()
        self.remove_element(original)
        new.set_designator(original_designator)
        self.add_element(new)

    def remove_element(self, element):
        """Remove element from this device."""
        #G.remove_node(element)
        #del Device.element_register[id(element)]
        pass

    def get_elements(self):
        """Return list of elements that owns to this device.

        .. note::

          This list will not include **all** the elements, but only neighbors of
          particular device on the graph.
        """
        elements = self.G.neighbors(self)
        return elements

    def find_element(self, by):
        """If there is more than one child matching the search, the first
        one is returned. In that case, :func:`find_elements` should be used.
        """
        elements = self.find_elements(by)
        if len(elements):
            return elements[0]
        return None

    def find_elements(self, by):
        """Returns elements of this device that is identified by `by`, or
        ``None`` if there is no such object.

        The by argument can be represented by a function, string, class or
        number. Omitting the by argument causes all object to be matched.
        """
        searcher = Device.Searcher(self.get_elements())
        return searcher.find_elements(by)

    def connect_to(self, element):
        """Connect two elements: this device and `element`. The connection
        between two elements is represented by edge on the graph :attr:`G`.
        """
        self.G.add_edge(self, element)

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

def verify_device(device):
    pass
