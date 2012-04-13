#!/usr/bin/env python

"""This module contains basic design primitives."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import copy

try:
    import networkx
except ImportError:
    print >>sys.stderr, "Please install networkx library:", \
        "http://networkx.lanl.gov"
    exit(1)
G = networkx.DiGraph()

class Property(object):
    """This class represents property of a primitive."""
    def __init__(self, name, value=None, groups=()):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

class Primitive(object):
    """This class is basic for any primitive.

    Each primitive has unique ID -- designator :attr:`Primitive.designator` for
    identification. By default the system tries to generate it with help of
    :attr:`Primitive.designator_format`. However it can be
    changed manually by using :attr:`Primitive.designator` property."""

    def __init__(self):
        self.__properties = dict()
        self.__owner = None
        self.__id = id(self)
        self.__designator_format = "P%d"
        self.__designator = None
        global G
        G.add_node(self)

    def clone(self):
        """Creates and returns a copy of this object. The default
        implementation returns a so-called "shallow" copy: It creates
        a new instance of the same class and then copies the field
        values (including object references) from this instance to the
        new instance. A "deep" copy, in contrast, would also
        recursively clone nested objects."""
        clone = self.__class__()
        for k, v in self.__dict__.iteritems():
            setattr(clone, k, v)
        return clone

    @property
    def designator_format(self):
        """Defines the format string to be used with the part
        designator. A reference designator unambiguously identifies a
        component in an electrical schematic (circuit diagram) or on a
        printed circuit board (PCB). The reference designator usually
        consists of one or two letters followed by a number, e.g. R13,
        C1002."""
        return self.__designator_format

    @designator_format.setter
    def designator_format(self, frmt):
        self.__designator_format = frmt

    @property
    def designator(self):
        """Designator is the name of a part on a printed circuit by
        convention beginning with one or two letters followed by a
        numeric value. The letter designates the class of component;
        eg. "Q" is commonly used as a prefix for transistors.

        It is very important to clearly understand the importance of
        the reference designator and the rules for assigning reference
        designators. An alphanumeric reference designator is used to
        uniquely identify each part. A given circuit might have ten
        1.0k resistors used in different locations. Each of these
        resistors is given a unique reference designator, for example,
        Rl, R5, and R7. In addition to the schematic, the reference
        designators also appear on the PCB legend silkscreen, assembly
        drawing, and bill of materials. Manufacturing uses the
        reference designators to determine where to stuff parts on the
        board. Field service uses them to identify and replace failed
        parts."""
        return self.__designator

    @designator.setter
    def designator(self, text):
        self.__designator = text

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def owner(self):
        """Returns a reference to the owner object."""
        return self.__owner

    @owner.setter
    def owner(self, primitive):
        self.__owner = primitive

    #def property(cls):
    #    pass

    def add_property(self, property):
        """Add a new property for the primitive."""
        if not isinstance(property, Property):
            raise Exception("Not a Property")
        if self.has_property(property):
            raise Exception("This property is already defined")
        self.__properties[property.name] = property

    def has_property(self, property_):
        property_name = property_
        if isinstance(property_, Property):
            property_name = property_.name
        return property_name in self.properties

    def set_property(self, name, value, group=None):
        property_ = self.get_property(name)
        if property_:
            property_.value = value
            return property_
        property_ = Property(name, value, group)
        self.add_property(property_)
        return property_

    def get_properties(self, group=None):
        """Return all the properties. See also :attr:`Primitive.properties`."""
        return self.properties

    def get_property(self, name):
        if not self.has_property(name):
            return None
        return self.properties[name]

    def get_property_value(self, name, default=None):
        property_ = self.get_property(name)
        if not property_:
            return default
        return self.get_property(name).value

    @property
    def properties(self):
        """Return all properties."""
        return self.__properties

class ElectronicPrimitive(Primitive):
    """This class represents basic electrical design primitive."""

class Pin(ElectronicPrimitive):
    """A pin is an electrical design primitive. Pins give a part its
    electrical properties and define connection points on the part for
    directing signals in and out."""

    class ElectricalTypes:
        """Class of possible electrical types."""
        Input = 0
        IO = 1
        Output = 2

    def __init__(self):
        ElectronicPrimitive.__init__(self)
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
        G.add_edge(self, pin)
        G.add_edge(pin, self)
        if not self.is_connected_to(pin):
            self._connections[id(pin)] = pin
            pin.connect_to(self)

    def is_connected_to(self, pin):
        return id(pin) in self._connections

class Note(Primitive):
    """A note is a design primitive (non-electrical). It is used to
    add informational or instructional text to a specific area within
    a schematic, in a similar vain to that of commenting a program's
    source code."""
    def __init__(self):
        Primitive.__init__(self)
        self.__text = ""

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text

class Wire(ElectronicPrimitive):
    """A wire is an electrical design primitive. It is an object that
    forms an electrical connection between points on a schematic and is
    analogous to a physical wire."""

    def __init__(self):
        ElectronicPrimitive.__init__(self)

    def connect(self, first_pin, second_pin):
        self.first_pin = first_pin
        self.second_pin = second_pin
        G.add_edge(first_pin, second_pin)
        G.add_edge(second_pin, first_pin)

    def find_pin(self, by):
        for pin in (self.first_pin, self.second_pin):
            if pin.designator == by:
                return pin

    def disconnect(self):
        self.first_pin = self.second_pin = None

    def get_first_pin(self):
        return self.first_pin

    def get_second_pin(self):
        return self.second_pin

    def clone(self):
        clone = ElectronicPrimitive.clone(self)
        clone.connect(self.get_first_pin().clone(), self.get_second_pin().clone())
        return clone

class Bus(ElectronicPrimitive):
    """A bus is an electrical design primitive. It is an object that represents
    a multi-wire connection."""
