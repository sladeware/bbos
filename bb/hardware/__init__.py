#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Base models for hardware abstraction."""

import types

import networkx

from bb.utils.type_check import verify_list, verify_string, verify_int, \
    is_list, is_dict, is_sequence

#_______________________________________________________________________________

class AppObject(object):
    pass

class Object(AppObject):
    def __init__(self, name):
        self.__name = name
        self.__properties = dict()

    def get_property(self, key, default_value=None):
        return self.__properties.get(key, default_value)

    def get_properties(self):
        return self.__properties

    def set_property(self, key, value):
        self.__properties[key] = value

    def get_name(self):
        return self.__name

class Autonaming(object):
    NAME_FORMAT = "OBJECT_%d"
    COUNTER_PER_LABEL_FORMAT = dict()

    def generate_name(self, format=None):
        if not format:
            format = self.NAME_FORMAT
        if not format in Autonaming.COUNTER_PER_LABEL_FORMAT:
            Autonaming.COUNTER_PER_LABEL_FORMAT[format] = 1
        counter = Autonaming.COUNTER_PER_LABEL_FORMAT[format]
        name = format % counter
        Autonaming.COUNTER_PER_LABEL_FORMAT[format] += 1
        return name

#_______________________________________________________________________________

class Connector(object):
    """Connector is a plug or receptacle which can be easily joined to
    or separated from its mate."""

    class Metadata(object):
        TYPE_MALE = "male"
        TYPE_FEMALE = "female"
        TYPE_WIRE = "wire"
        TYPE_PAD = "pad"
        TYPE_UNKNOWN = "unknown"

        def __init__(self):
            self.__name = None
            self.__type = self.TYPE_UNKNOWN
            self.__description = None
            self.__number = None

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, name):
            self.__name = name

        @property
        def number(self):
            return self.__number

        @number.setter
        def number(self, number):
            self.__number = number

        @property
        def description(self):
            return self.__description

        @description.setter
        def description(self, text):
            self.__description = text

        @property
        def type(self):
            return self.__type

        @type.setter
        def type(self, type_):
            self.__type = type_

    def __init__(self):
        self.metadata = self.Metadata()
        self._connectors = dict()

    def connect_to(self, connector):
        """Connect source connector to destination connector."""
        if not self.is_connected_to(connector):
            self._connectors[connector.metadata.number] = connector
            connector.connect_to(self)

    def is_connected_to(self, connector):
        return connector.metadata.number in self._connectors

def is_connector(connector):
    return isinstance(connector, Connector)

def verify_connector(connector):
    if not is_connector(connector):
        raise Exception()
    return connector

#_______________________________________________________________________________

class Sketch(object):

    # Public variable that keeps an instance of currently active sketch
    active_instance = None

    # Complete list of all parts from all sketches. The part can not
    # belong to more than one sketch.
    all_parts = dict()

    def __init__(self):
        Sketch.active_instance = self
        self.__g = networkx.Graph()

    @classmethod
    def get_active_instance(cls):
        return Sketch.active_instance

    def add_part(self, part):
        if self.has_part(part):
            return part
        if id(part) in self.all_parts:
            raise Exception("The part '%s' already belongs to '%s' sketch" \
                                % (part, self.all_parts[id(part)]))
        self.all_parts[id(part)] = self
        self.__g.add_node(part)
        return part

    def remove_part(self, part):
        pass

    def has_part(self, part):
        return self.__g.has_node(part)

    def connect(self, part1, part2):
        Sketch.active_instance = self
        for part in (part1, part2):
            self.add_part(part)
        self.__g.add_edge(part1, part2)

    def disconnect(self, part1, part2):
        pass

    def has_connection(self, part1, part2):
        Sketch.active_instance = self
        return self.__g.has_edge(part1, part2)

    def find_part(self, by=None, type=None):
        """Returns the part of this sketch that is an instance of
        type and that is identified by by, or None if there is no such
        object.

        The by argument can be represented by a function, string or
        number. Omitting the by argument causes all object to be
        matched.

        If there is more than one child matching the search, the first
        one is returned. In that case, Part.find_children() should be used."""
        parts = self.find_parts(by, type)
        if parts:
            return parts.pop(0)
        return None

    def find_parts(self, by=None, type=None):
        parts = list()
        if not type:
            type = Part
        for part in self.__g.nodes():
            if isinstance(part, type):
                parts.append(part)
        return parts

#_______________________________________________________________________________

class Part(object):

    class Properties(object):
        """"This class describes part's technical
        characteristics. It includes all of the distinguishing features that
        make your part unique."""

    class Metadata(object):
        """This class keeps metadata information for Part."""
        def __init__(self):
            self.__author = None
            self.__name = None
            self.__version = "0.0.0"
            self.__description = None
            self.__reference_format = "Part"
            self.__keywords = list()

        @property
        def keywords(self):
            """A list of additional keywords to be used to assist
            searching for the package in a larger catalog. This makes
            the part findable."""
            return self.__keywords

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, name):
            self.__name = name

        @property
        def reference_format(self):
            """See Part.reference"""
            return self.__reference_format

        @reference_format.setter
        def reference_format(self, frmt):
            self.__reference_format = frmt

        @property
        def description(self):
            """A longer description of the part that can run to
            several paragraphs."""
            return self.__description

        @description.setter
        def description(self, text):
            self.__description = text

        @property
        def version(self):
            return self.__version

        @version.setter
        def version(self, version):
            self.__version = version

        @property
        def author(self):
            """A string containing the author's name at a minimum; additional
            contact information may be provided."""
            return self.__author

        @author.setter
        def author(self, name):
            self.__author = name

    def __init__(self, *args):
        self.__reference = None
        self.__id = id(self)
        self.__connectors = dict()
        self.__properties = self.Properties()
        # Store the part meta-data (name, version, author, and so
        # forth) in a separate object -- we're getting to have enough
        # information here that it's worth it.
        self.__metadata = self.Metadata()

    @property
    def metadata(self):
        return self.__metadata

    @property
    def properties(self):
        return self.__properties

    def add_connector(self, connector):
        if self.has_connector(connector):
            raise Exception("'%s' already has connector '%s'" \
                                % (self.metadata.name, connector.metadata.name))
        self.__connectors[connector.metadata.number] = connector

    def has_connector(self, connector):
        return connector.metadata.name in self.__connectors

    def find_connector(self, number):
        return self.__connectors.get(number, None)

    def get_num_connectors(self):
        return len(self.get_connectors())

    def get_connectors(self):
        return self.__connectors.values()

    @property
    def reference(self):
        """Reference designator (abbrv. "ref des") -- The name of a
        component on a printed circuit by convention beginning with
        one or two letters followed by a numeric value. The letter
        designates the class of component; eg. "Q" is commonly used as
        a prefix for transistors."""
        return self.__reference

    @reference.setter
    def reference(self, value):
        self.__reference = value

    def get_id(self):
        return self.__id

    def set_id(self, identifier):
        self.__id = identifier

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object."""
        return "Part %s" % self.get_name()

#_______________________________________________________________________________

class Device(Part):
    """This class represents any kind of electronic devices.

    Every single device within a board has unique name or label. If
    the name wasn't provided it will be generated automatically. This
    allows you to control these devices from operating system. For
    example, if you have an led called LED1, it can be blinked as
    follows:

    kernel.control_device("LED1", "BLINK")"""

    def __init__(self, name=None):
        Part.__init__(self, name)

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object."""
        return "Device %s" % self.name

def is_device(instance):
    return isinstance(instance, Device)

def verify_device(instance):
    if not is_device(instance):
        raise TypeError("Not a device.")
    return instance

