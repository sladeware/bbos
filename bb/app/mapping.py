#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.hardware import Device
from bb.hardware.parts.boards import Board
from bb.hardware.parts.processors import Processor

#_______________________________________________________________________________

class _Hardware(object):
    """This class represents interface between a single mapping and hardware
    abstraction layer."""

    def __init__(self):
        self.__core = None

    def is_board_defined(self):
        return not not self.get_board()

    def get_board(self):
        """Return Board instance."""
        return self.get_processor().get_owner()

    def is_processor_defined(self):
        """Whether or not a processor was defined. Return True value if the
        processor's instance can be obtained by using specified core. Otherwise
        return False."""
        return not not self.get_processor()

    def get_processor(self):
        """Return Processor instance."""
        if not self.get_core():
            return None
        return self.get_core().get_owner()

    def is_core_defined(self):
        """Whether or not a core was defined."""
        return not not self.get_core()

    def set_core(self, core):
        if not isinstance(core, Processor.Core):
            raise TypeError("Core must be %s sub-class" %
                            Processor.Core.__class__.__name__)
        self.__core = core

    def get_core(self):
        """Return Core instance."""
        return self.__core

#______________________________________________________________________________

class Mapping(object):
    def __init__(self, name, os_class=None, build_params=None):
        self.name = name
        self.build_params = build_params or dict()
        self.hardware = _Hardware()
        if os_class:
            self.os_class = os_class
        elif hasattr(self, "os_class"):
            self.os_class = getattr(self, "os_class")

    def __str__(self):
        return "Mapping %s" % self.name

    def __repr__(self):
        return str(self)

def verify_mapping(mapping):
    if not isinstance(mapping, Mapping):
        raise TypeError("Unknown mapping '%s'. "
                        "Not a subclass of bb.mapping.Mapping class" %
                        (mapping))
    return mapping
