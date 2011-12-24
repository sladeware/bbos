#!/usr/bin/env python

"""This module contains basic design primitives."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_______________________________________________________________________________

class Property(object):
    """This class represents property of a primitive."""
    def __init__(self, name, value=None, groups=()):
        self.__name = name
        self.__value = value
        self.__groups = ()

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

#_______________________________________________________________________________

class Primitive(object):
    """This class is basic for any primitive.

    Each primitive has unique ID -- designator `Primitive.designator` for
    identification. By default the system tries to generate it with help of
    `Primitive.designator_format`. However it can be
    changed manually by using `Primitive.designator` property."""

    def __init__(self):
        self.__properties = dict()
        self.__owner = None
        self.__id = id(self)
        self.__designator_format = "P%d"
        self.__designator = None

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
        """Return all the properties. See also `Primitive.properties`."""
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

#_______________________________________________________________________________

class ElectricalPrimitive(Primitive):
    """This class represents basic electrical design primitive."""

#_______________________________________________________________________________

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

class Model(Primitive):
    def __init__(self):
        """By default designator is None."""
        Primitive.__init__(self)

