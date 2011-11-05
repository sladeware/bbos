#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Base things for hardware abstraction."""

import types

from bb.hardware.device import Device
from bb.hardware.processor import Processor
from bb.hardware.core import Core

from bb.utils.type_check import verify_list, is_list, is_dict

class Board(Device):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BBOS does not explicitly refer to them."""

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

class Hardware(object):
    """This class represents interface between a single mapping and hardware
    abstraction."""
    def __init__(self):
        self.__core = None

    def get_board(self):
        return self.get_processor().get_owner()

    def is_processor_defined(self):
        """Whether or not a processor was defined. Return True value if the
        processor's instance can be obtained by using specified core. Otherwise
        return False."""
        if not self.get_core():
            return False
        return not not self.get_processor()

    def get_processor(self):
        return self.__core.get_owner()

    def is_core_defined(self):
        """Whether or not a core was defined."""
        return not not self.get_core()

    def set_core(self, core):
        if not isinstance(core, Core):
            raise TypeError("Core must be %s sub-class", Core.__class__.__name__)
        self.__core = core

    def get_core(self):
        return self.__core
