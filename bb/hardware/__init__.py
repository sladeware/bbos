#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Base models for hardware abstraction."""

import types

from bb.utils.type_check import verify_list, verify_string, is_list, is_dict

#_______________________________________________________________________________

class Device(object):
    LABEL_FORMAT = "DEVICE_%d"
    COUNTER_PER_LABEL_FORMAT = dict()

    def __init__(self, label=None):
        self.__label = None
        if not label:
            label_format = self.LABEL_FORMAT
            if not label_format in Device.COUNTER_PER_LABEL_FORMAT:
                Device.COUNTER_PER_LABEL_FORMAT[label_format] = 1
            counter = Device.COUNTER_PER_LABEL_FORMAT[label_format]
            label = label_format % counter
            Device.COUNTER_PER_LABEL_FORMAT[label_format] += 1
        self.set_label(label)

    def get_label(self):
        return self.__label

    def set_label(self, label):
        self.__label = verify_string(label)

    def power_on(self):
        raise NotImplemented("What the device should do when the power is on?")

    def power_off(self):
        raise NotImplemented()

    def get_owner(self):
        return self.__owner

    def set_owner(self, owner):
        self.__owner = owner

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object."""
        return "Device %s" % self.get_label()

def verify_device(part):
    if not isinstance(part, Part):
        raise TypeError("Not a Part.")

#_______________________________________________________________________________

class Core(Device):
    """Base class used to represent a core within a processor.

    A Core is the smallest computational unit supported by BB. There is one
    core per processes and one process per core."""
    def __init__(self, name, mapping=None):
        Device.__init__(self, name)
        self.__mapping = None
        self.__owner = None
        if mapping:
            self.set_mapping(mapping)

    def power_on(self):
        if not self.get_mapping():
            return

    def set_mapping(self, mapping):
        from bb.app import Mapping
        if not isinstance(mapping, Mapping):
            print isinstance(mapping, Mapping)
            raise TypeError('mapping %s must be %s sub-class'
                            % (mapping, Mapping.__class__.__name__))
        self.__mapping = mapping
        mapping.hardware.set_core(self)

    def get_mapping(self):
        return self.__mapping

class Processor(Device):
    """Base class used for creating a BB processor.

    A processor contains one or more cores. It is a discrete semiconductor
    based device used for computation. For example, the PIC32MX5
    microcontroller is a processor."""

    def __init__(self, name, num_cores=0, cores=None):
        Device.__init__(self, name)
        if num_cores < 1:
            raise NotImplemented("Number of cores must be more than zero.")
        self.__num_cores = num_cores
        self.__cores = {}
        if cores:
            self.set_cores(cores)
        self.__owner = None

    def power_on(self):
        """Power on processor and its cores one by one."""
        for id, core in self.get_cores():
            core.power_on()

    def set_cores(self, cores):
        """Set a bunch of cores at once. The set of cores can be represented by
        a list (in this case processor's position in this list will be its ID)
        and by a dict (the key represents processor's ID and value - processor's
        instance)."""
        if is_list(cores) and len(cores):
            for i in range(len(cores)):
                self.set_core(cores[i], i)
        elif is_dict(cores) and len(cores):
            for id, core in cores.items():
                self.set_core(core, id)

    def set_core(self, core, id):
        """Set a processor's core associated with specified identifier. If the
        core with such ID is already presented, it will be replaced."""
        if not isinstance(core, Core):
            raise TypeError('core "%s" must be bb.os.Core sub-clas' % core)
        self.validate_core(core)
        self.validate_core_id(id)
        self.__cores[id] = core
        core.set_owner(self)

    def get_core(self, id=0):
        """Get processor's core. If core's ID is not selected, will be returned
        the first core with 0 ID."""
        self.validate_core_id(id)
        return self.__cores[id]

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplemented

    def is_valid_core(self, core):
        return True

    def validate_core_id(self, i):
        if self.get_num_cores() <= i:
            raise NotImplemented('The %s supports up to %d cores. '
                                 'You have too many: %d' %
                                 (self.__class__.__name__,
                                  self.get_num_cores(), i))

    def get_cores(self):
        return self.__cores.items()

    def get_num_cores(self):
        return self.__num_cores

    def get_mappings(self):
        mappings = []
        for core in self.get_cores():
            if not core:
              continue
            mappings.append(core.get_mapping())
        return mappings

class Board(Device):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BB does not explicitly refer to them."""

    def __init__(self, name, num_processors, processors=[]):
        Device.__init__(self, name)
        self.__num_processors = num_processors
        self.__processors = {}
        self.__devices = []
        # Set and verify the list of processors on this board
        if processors:
            self.set_processors(processors)

    def get_devices(self):
        return self.__devices

    def add_device(self, device):

        self.__devices.append(device)

    def remove_device(self, device):
        pass

    def find_device_by_name(self, name):
        pass

    def find_device_by_class(self, klass):
        pass

    def power_on(self):
        """Power on this board."""
        for (id, processor) in self.get_processors():
            processor.power_on()

    def set_processors(self, processors):
        # A set of processors is represented by a list
        if is_list(processors) and len(processors):
            for i in range(len(processors)):
                self.set_processor(processors[i], i)
        # A set of processors is represented by a dict
        elif is_dict(processors) and len(processors):
            for id, processor in processors.items():
                self.set_processor(processor, id)

    def set_processor(self, processor, i=0):
        """Set a processor with specified identifier."""
        if not isinstance(processor, Processor):
            raise TypeError('processor "%s" must be bb.os.hardware.Processor'
                            'sub-class' % processor)
        self.validate_processor(processor)
        self.validate_processor_id(i)
        processor.set_owner(self)
        self.add_device(processor)
        self.__processors[i] = processor
        processor.set_owner(self)

    def get_processor(self, i=0):
        self.validate_processor_id(i)
        return self.__processors[i]

    def validate_processor_id(self, n):
        if self.get_num_processors() < n:
            raise NotImplemented

    def validate_processor(self, processor):
        if not self.is_valid_processor(processor):
            raise NotImplemented

    def is_valid_processor(self, processor):
        """Board specific method. Checks whether or not particular processor
        can be placed on this board."""
        return True

    def get_num_processors(self):
        """Returns number of processors that can be placed on this board."""
        return self.__num_processors

    def get_processors(self):
        """Returns a list of processors."""
        return self.__processors.items()

    def get_mappings(self):
        """Collect and return mappings from all processors."""
        mappings = []
        for processor in self.get_processors():
            mappings.extend(processor.get_mappings())
        return mappings

