#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.eda.devices import Device
from bb.utils.type_check import is_sequence, verify_int

#_______________________________________________________________________________

class Processor(Device):
    """Base class used for creating a processor. It is a discrete
    semiconductor based device used for computation. For example, the
    PIC32MX5 microcontroller is a processor.

    A processor contains one or more cores, where each is represented by
    a Processor.Core. All the cores a enumerated.

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

    class Core(object):
        """Base class used to represent a core within a processor. In
        comparison to another hardware components, core is not a Device
        since it can not be reused outside of processor. Thus it's a part
        of processor.

        A Core is the smallest computational unit supported by BB. There
        is one core per process and one process per core. It connects
        outside world with mapping, that allows operating system to all
        ather devices."""

        def __init__(self, mapping=None):
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

    def __init__(self, num_cores=0, cores=None):
        Device.__init__(self)
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
        verify_int(id)
        self.verify_core(core)
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

    def verify_core(self, core):
        if not isinstance(core, Processor.Core):
            raise TypeError('core "%s" must be bb.os.Core sub-class' % core)
        return core

    def validate_core(self, core):
        if not self.is_valid_core(core):
            raise NotImplementedError()

    def is_valid_core(self, core):
        """This method has to be rewriten for a proper processor. For
        example for PropellerP8X32 processor we are always waiting for
        PropellerCog core. By default it simply reuses is_core()
        function."""
        return self.verify_core(core) #is_core(core)

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
