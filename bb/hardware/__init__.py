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

class Connector(Object):
    TYPE_MALE = "male"
    TYPE_FEMALE = "female"
    TYPE_WIRE = "wire"
    TYPE_PAD = "pad"
    TYPE_UNKNOWN = "unknown"

    def __init__(self, name, type):
        Object.__init__(self, name)
        self.type = type

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

class Part(Object):

    def __init__(self, name=None):
        Object.__init__(self, name)
        self.__connectors = dict()

    def add_connector(self, connector):
        verify_connector(connector)
        if self.has_connector(connector):
            raise Exception("This connector was already defined")
        self.__connectors[connector.get_name()] = connector

    def has_connector(self, connector):
        return connector.get_name() in self.__connectors

    def find_connector(self, name):
        verify_string(name)
        return self.__connectors[name]

    def get_connectors(self):
        return self.__connectors.values()

    def get_num_connectors(self):

        return len(self.get_connectors())

    def remove_connector(self, connector):
        raise

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
        return "Device %s" % self.get_name()

def is_device(instance):
    return isinstance(instance, Device)

def verify_device(instance):
    if not is_device(instance):
        raise TypeError("Not a device.")
    return device

#_______________________________________________________________________________

class Core(Object):
    """Base class used to represent a core within a processor. In
    comparison to another hardware components, core is not a Device
    since it can not be reused outside of processor. Thus it's a part
    of processor.

    A Core is the smallest computational unit supported by BB. There
    is one core per process and one process per core. It connects
    outside world with mapping, that allows operating system to all
    ather devices."""

    def __init__(self, name, mapping=None):
        Object.__init__(self, name)
        self.__processor = None
        self.__mapping = None
        if mapping:
            self.set_mapping(mapping)

    def get_processor(self):
        return self.__processor

    def set_processor(self, processor):
        self.__processor = processor

    def set_mapping(self, mapping):
        """Connects core with mapping. Once they are connected, the
        mapping can see the core and other devices through hardware
        reflector if such were defined."""
        from bb.app import Mapping, verify_mapping
        self.__mapping = verify_mapping(mapping)
        mapping.hardware.set_core(self)

    def get_mapping(self):
        """Returns Mapping associated with this core. By default
        returns None."""
        return self.__mapping

def is_core(core):
    """Returns True if specified variable is a Core."""
    return isinstance(core, Core)

def verify_core(core):
    if not is_core(core):
        raise TypeError('core "%s" must be bb.os.Core sub-class' % core)
    return core

#_______________________________________________________________________________

class Processor(Device):
    """Base class used for creating a processor. It is a discrete
    semiconductor based device used for computation. For example, the
    PIC32MX5 microcontroller is a processor.

    A processor contains one or more cores, where each is represented by
    a Core. All the cores a enumerated.

    The following example shows how to define a processor with a
    single core on it:

    processor = Processor("MyProcessor", 1, (Core("MyCore")))
    core = processor.get_core() # or processor.get_core(0)

    The composition and balance of the cores in multi-core processor
    show great variety. Some architectures use one core design
    repeated consistently ("homogeneous"), while others use a mixture
    of different cores, each optimized for a different,
    "heterogeneous" role. Homogeneous multi-core systems include only
    identical cores, heterogeneous multi-core systems have cores which
    are not identical. The Processor.validate_core() and
    Processor.is_valid_core() can be reused in order to provide core
    validation."""

    def __init__(self, name, num_cores=0, cores=None):
        Device.__init__(self, name)
        if num_cores < 1:
            raise Exception("Number of cores must be greater than zero.")
        self.__num_cores = num_cores
        self.__cores = [None] * num_cores
        if cores:
            self.set_cores(cores)

    def set_cores(self, cores):
        """Set a bunch of cores at once. The set of cores can be
        represented by any sequence (in this case processor's position in
        this list will be its ID) and by a dict (the key represents
        processor's ID and value - processor's instance)."""
        if is_sequence(cores) and len(cores):
            for i in range(len(cores)):
                self.set_core(cores[i], i)
        elif is_dict(cores) and len(cores):
            for id, core in cores.items():
                self.set_core(core, id)
        else:
            raise Exception("Cores is not a sequnce or dictionary.")

    def set_core(self, core, id):
        """Set a processor's core associated with specified
        identifier. If the core with such ID is already presented, it
        will be replaced."""
        verify_core(core)
        verify_int(id)
        self.validate_core(core)
        self.validate_core_id(id)
        self.__cores[id] = core

    def get_core(self):
        """Returned the first core Core with ID 0."""
        return self.find_core(0)

    def find_core(self, by):
        """Find processor's core by an index or name."""
        self.validate_core_id(by)
        return self.__cores[by]

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplementedError()

    def is_valid_core(self, core):
        """This method has to be rewriten for a proper processor. For
        example for PropellerP8X32 processor we are always waiting for
        PropellerCog core. By default it simply reuses is_core()
        function."""
        return is_core(core)

    def validate_core_id(self, i):
        """Validates core ID, which has to be less than the total
        number of cores and greater or equal to zero."""
        if i >= 0 and self.get_num_cores() <= i:
            raise Exception('The %s supports up to %d cores. '
                            'You have too many: %d' %
                            (self.__class__.__name__,
                             self.get_num_cores(), i))

    def get_cores(self):
        """Returns all the cores."""
        return self.__cores

    def get_num_cores(self):
        return self.__num_cores

    def get_mappings(self):
        """Returns a list of mappings managed by this processor. Each
        mapping is taken from appropriate core."""
        mappings = list()
        for core in self.get_cores():
            if not core:
              continue
            mappings.append(core.get_mapping())
        return mappings

def verify_processor(processor):
    if not isinstance(processor, Processor):
        raise TypeError('processor "%s" must be bb.os.hardware.Processor'
                        'sub-class' % processor)
    return processor

#_______________________________________________________________________________

class Breadboard(Device):
    pass

class Board(Device):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may
    not be the same, depending on the board. A board is a piece of
    hardware that performs computation within its processors. Other
    supporting hardware may be present on the board, but BB does not
    explicitly refer to them."""

    def __init__(self, name):
        Device.__init__(self, name)

