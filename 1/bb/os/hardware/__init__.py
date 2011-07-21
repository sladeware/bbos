#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

"""Hardware abstraction"""

import types

from bb.apps.utils.type_verification import verify_list
from bb.apps.utils.distribution import DistributionMetadata
from bb.os.kernel import Kernel, Module
from bb import app

#______________________________________________________________________________

class Driver(Module):
    def __init__(self):
        Module.__init__(self)

#______________________________________________________________________________

class Core(DistributionMetadata):
    """Base class used to represent a core within a processor.

    A Core is the smallest computational unit supported by BBOS. There is one
    core per processes and one process per core."""

    __process = None
    __owner = None

    def __init__(self, name, process=None):
        DistributionMetadata.__init__(self, name)
        if process:
            self.set_process(process)

    def set_process(self, process):
        if not isinstance(process, app.Process):
            raise TypeError('process must be %s sub-class' 
                            % app.Process.__class__.__name__)
        self.__process = process
        process.get_hardware().set_core(self)

    def get_process(self):
        return self.__process

    def get_owner(self):
        return self.__owner

    def set_owner(self, processor):
        self.__owner = processor

#______________________________________________________________________________

class Processor(DistributionMetadata):
    """Base class used for creating a BBOS processor.

    A processor contains one or more cores. It is a discrete semiconductor
    based device used for computation. For example, the PIC32MX5 
    microcontroller is a processor."""
    
    __cores = []
    __number_of_cores = 0
    __owner = None

    def __init__(self, name, number_of_cores=0, cores=[]):
        DistributionMetadata.__init__(self, name)
        if number_of_cores < 1:
            raise NotImplemented("Number of cores must be more than zero.")
        self.__number_of_cores = number_of_cores
        self.__cores = [None] * number_of_cores
        if cores:
            self.set_cores(cores)

    # Owner Management

    def set_owner(self, board):
        self.__owner = board

    def get_owner(self):
        return self.__owner

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
        core.set_owner(self)

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

    def get_number_of_cores(self):
        return self.__number_of_cores

    # Process Management

    def get_processes(self):
        processes = []
        for core in self.get_cores():
            processes.append(core.get_process())
        return processes

#______________________________________________________________________________

class Board(DistributionMetadata):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may not be
    the same, depending on the board. A board is a piece of hardware that
    performs computation within its processors. Other supporting hardware
    may be present on the board, but BBOS does not explicitly refer to them."""

    __processors = []
    __number_of_processors = 0

    def __init__(self, name, number_of_processors, processors=[]):
        DistributionMetadata.__init__(self, name)
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
        processor.set_owner(self)

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

