#!/usr/bin/env python

from bb.lib.utils import typecheck

__all__ = ["Primitive", "ElectronicPrimitive"]

class Primitive(object):
    DESIGNATOR_FORMAT="P%d"

    PROPERTIES = ()

    class Property(object):

        def __init__(self, name, value=None):
            self._name = name
            self._value = value

        @property
        def name(self):
            return self._name

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, new_value):
            self._value = new_value


    def __init__(self, designator=None, designator_format=None):
        self._properties = dict()
        self._id = id(self)
        self._designator_format = None
        self._designator = None
        if designator_format:
            self.set_designator_format(designator_format)
        else:
            self.set_designator_format(self.DESIGNATOR_FORMAT)
        if designator:
            self.set_designator(designator)
        else:
            self.generate_designator()
        if self.PROPERTIES:
            self.add_properties(self.PROPERTIES)

    def clone(self):
        clone = self.__class__()
        for k, v in self.__dict__.iteritems():
            setattr(clone, k, v)
        return clone

    def get_designator_format(self):
        return self._designator_format

    def generate_designator(self, counter=0):
        designator = self.get_designator_format() % counter
        self.set_designator(designator)
        return designator

    def set_designator_format(self, frmt):
        self._designator_format = frmt

    def get_designator(self):
        return self._designator

    def set_designator(self, text):
        # TODO(team): designator should be unique within its graph
        self._designator = text

    def get_id(self):
        return self._id

    def set_id(self, value):
        self._id = value

    def add_properties(self, properties):
        if not typecheck.is_sequence(properties):
            raise TypeError("Has to be list")
        for property in properties:
            self.add_property(property)

    def add_property(self, property):
        if not isinstance(property, Primitive.Property):
            raise Exception("Not a Property")
        self._properties[property.name] = property

    def has_property(self, property_):
        property_name = property_
        if isinstance(property_, Primitive.Property):
            property_name = property_.name
        return property_name in self._properties

    def set_property(self, name, value):
        property_ = self.get_property(name)
        if property_:
            property_.value = value
            return property_
        property_ = Primitive.Property(name, value)
        self.add_property(property_)
        return property_

    def get_properties(self):
        return self._properties.values()

    def get_property(self, name):
        if not self.has_property(name):
            return None
        return self._properties[name]

    def get_property_value(self, name, default=None):
        property_ = self.get_property(name)
        if not property_:
            return default
        return self.get_property(name).value

    def __str__(self):
        return "Primitive <%s>" % self.get_designator()


class ElectronicPrimitive(Primitive):
    pass
