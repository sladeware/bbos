#!/usr/bin/env python

"""Hardware abstraction"""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import types

#______________________________________________________________________________

class Board(object):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BBOS does not explicitly refer to them."""

    __processors = []
    __number_of_processors = 0

    def __init__(self, name, number_of_processors, processors=[]):
        self.__number_of_processors = number_of_processors
        # By default will be created a list of None's
        self.__processors = [None] * number_of_processors
        # Set and verify the list of processors on this board
        if processors:
            self.set_processors(processors)

    # Processor Management

    def set_processors(self, processors):
        verify_list(processors)
        for i in range(len(processors)):
            self.set_processor(processors[i], i)

    def set_processor(self, processor, i=0):
        """Set a processor with specified identifier."""
        if not isinstance(processor, Processor):
            raise TypeError('processor "%s" must be bb.os.hardware.Processor'
                            'sub-class' % processor)
        self.validate_processor(processor)
        self.validate_processor_id(i)
        processor.set_owner(self)
        self.__processors[i] = processor

    def get_processor(self, i=0):
        self.validate_processor_id(i)
        return self.__processors[i]

    def validate_processor_id(self, n):
        if self.get_number_of_processors() < n:
            raise NotImplemented

    def validate_processor(self, processor):
        if not self.is_valid_processor(processor):
            raise NotImplemented

    def is_valid_processor(self, processor):
        """Board specific method. Checks whether or not particular processor 
        can be placed on this board."""
        return True

    def get_number_of_processors(self):
        """Returns number of processors that can be placed on this board."""
        return self.__number_of_processors

    def get_processors(self):
        """Returns a list of processors."""
        return self.__processors

    # Process Management

    def get_processes(self):
        """Collect and return processes from all processors."""
        processes = []
        for processor in self.get_processors():
            processes.extend(processor.get_processes())
        return processes

#______________________________________________________________________________

class Processor(object):
    """
    Base class used for creating a BBOS processor.

    A processor contains one or more cores. It is a discrete semiconductor based
    device used for computation. For example, the PIC32MX5 microcontroller is a
    processor.
    """
    
    __cores = []
    __number_of_cores = 0

    def __init__(self, name, number_of_cores=0, cores=[]):
        if number_of_cores < 1:
            raise NotImplemented("Number of cores must be more than zero.")
        self.__number_of_cores = number_of_cores
        self.cores = [None] * number_of_cores
        if cores:
            self.set_cores(cores)

    # Core Management

    def set_cores(self, cores):
        verify_list(cores)
        for i in range(len(cores)):
            self.set_core(cores[i], i)

    def set_core(self, core, i):
        if not isinstance(core, Core):
            raise TypeError('core "%s" must be bb.os.Core sub-clas' % core)
        self.validate_core(core)
        self.validate_core_id(i)
        self.__cores[i] = core

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplemented

    def is_valid_core(self, core):
        return True

    def validate_core_id(self, i):
        if self.get_number_of_cores() <= i:
            raise NotImplemented('The %s supports up to %d processes. '
                                 'You have too many: %d' % 
                                 (self.__class__.__name__, self.get_number_of_cores(), i))

    def get_cores(self):
        return self.__cores

    # Process Management

    def get_processes(self):
        processes = []
        for core in self.get_cores():
            processes.append(core.get_process())
        return processes

#______________________________________________________________________________

class Core(object):
    """Base class used to represent a core within a processor.

    A Core is the smallest computational unit supported by BBOS. There is one
    core per processes and one process per core."""

    __process = None

    def __init__(self, name, process=None):
        if process:
            self.set_process(process)

    def set_process(self, process):
        if not isinstance(process, Kernel):
            raise TypeError('process must be bb.os.kernel.Kernel sub-class' 
                            % process)
        self.__process = process

    def get_process(self):
        return self.__process

#______________________________________________________________________________

from bb.os.kernel import Module

class Driver(Module):
    pass

#______________________________________________________________________________

class Hardware(object):
    """Hardware abstraction"""
    def __init__(self):
        self.__board = None
        self.__processor = None
        self.__core = None
        self.__drivers = {}

    def set_board(self, board):
        if not isinstance(board, Board):
            raise TypeError('Board must be bb.os.hardware.Board sub-class')
        self.__board = board

    def set_processor(self, processor):
        if not isinstance(processor, Processor):
            raise TypeError('Processor must be bb.os.hardware.Processor '
                            'sub-class')
        self.__processor = processor

    def set_core(self, core):
        if not isinstance(core, Core):
            raise TypeError('Core must be bb.os.hardware.Core sub-class')
        self.__core = core

    def add_driver(self, driver):
        if not isinstance(driver, Driver):
            raise TypeError('Driver must be bb.os.hardware.Driver sub-class')
        self.__drivers[ driver.get_name() ] = driver

    def has_driver(self, *arg_list):
        if type(arg_list[0]) is types.StringType:
            return not self.find_driver(arg_list[0]) is None
        elif isinstance(arg_list[0], Driver):
            return not self.find_driver(arg_list[0].get_name()) is None

    def find_driver(self, name):
        if not type(name) is types.StringType:
            raise TypeError("Driver name must be a string")
        if name in self.__drivers:
            return self.__drivers[name]
        return None

    def remove_driver(self, *arg_list):
        raise NotImplemented()

