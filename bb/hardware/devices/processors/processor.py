#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Processor is a discrete semiconductor based device used for computation. For
example, the PIC32MX5 microcontroller is a processor. Each processor has
at least one :class:`Processor.Core`.

The following example shows how to define a processor with a single core on it::

    processor = Processor("MyProcessor", 1, (Core("MyCore")))
    core = processor.get_core() # or processor.get_core(0)
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

from bb.hardware.primitives import ElectronicPrimitive
from bb.hardware.devices import Device
from bb.utils.type_check import is_sequence, validate

class Processor(Device):
    """Base class used for creating a processor, that is derived from
    :class:`bb.hardware.devices.device.Device` class. A processor contains one
    or more cores described by `cores`, where each is represented by a
    :class:`Processor.Core`. All the cores a enumerated.

    The composition and balance of the cores in multi-core processor show great
    variety. Some architectures use one core design repeated consistently
    ("homogeneous"), while others use a mixture of different cores, each
    optimized for a different, "heterogeneous" role. Homogeneous multi-core
    systems include only identical cores, heterogeneous multi-core systems have
    cores which are not identical. The :func:`validate_core` and
    :func:`is_valid_core` can be reused in order to provide core validation.

    .. note:: Base :class:`Core` class is derived from
      :class:`bb.hardware.primitives.ElectronicPrimitive` but it can be more
      complicated and can be derived from
      :class:`bb.hardware.devices.device.Device`.
    """

    class Core(ElectronicPrimitive):
        """Base class used to represent a core within a processor and derived
        from :class:`bb.hardware.primitives.ElectronicPrimitive`. In comparison
        to another hardware components, core is not a
        :class:`bb.hardware.devices.device.Device` since it can not be reused
        outside of processor. Thus it's a part of processor.

        A :class:`Processor.Core` is the smallest computational unit supported
        by BB. There is one core per process and one process per core. It
        connects outside world with :class:`bb.app.mapping.Mapping` that is
        passed via `mapping`, that allows operating system to all ather devices.
        """

        def __init__(self, id_=None, mapping=None):
            ElectronicPrimitive.__init__(self)
            self.__processor = None
            self.__mapping = None
            if not id_ is None:
                self.set_id(id_)
            if mapping:
                self.set_mapping(mapping)

        def get_processor(self):
            """Return :class:`Processor` instance that owns this
            :class:`Processor.Core`.
            """
            return self.__processor

        def set_processor(self, processor):
            """Set :class:`Processor` that will control this
            :class:`Processor.Core`.
            """
            self.__processor = processor

        def set_mapping(self, mapping):
            """Connects :class:`Processor.Core` with `mapping`. Once they are
            connected, the mapping can see the core and other devices through
            :class:`bb.app.mapping.HardwareAgent` if such were defined.
            """
            from bb.app import Mapping, verify_mapping
            self.__mapping = verify_mapping(mapping)
            mapping.hardware.set_core(self)

        def get_mapping(self):
            """Returns :class:`bb.app.mapping.Mapping` associated with this
            core. By default returns ``None``.
            """
            return self.__mapping

    @validate(num_cores=int)
    def __init__(self, num_cores=0, cores=None):
        Device.__init__(self)
        if num_cores < 1:
            raise Exception("Number of cores must be greater than zero.")
        self.__num_cores = num_cores
        self.__cores = [None] * num_cores
        if cores:
            self.set_cores(cores)

    @validate(cores=is_sequence)
    def set_cores(self, cores):
        """Set a bunch of cores at once. The set of cores can be represented by
        any sequence (in this case processor's position in this list will be its
        ID) and by a dict (the key represents processor's ID and value -
        processor's instance).
        """
        if is_sequence(cores) and len(cores):
            for i in range(len(cores)):
                self.set_core(cores[i], i)
        elif is_dict(cores) and len(cores):
            for id, core in cores.items():
                self.set_core(core, id)
        else:
            raise Exception("Cores is not a sequnce or dictionary.")

    def set_core(self, core, id):
        """Set a processor's core associated with specified identifier. If the
        core with such ID is already presented, it will be replaced.
        """
        self.verify_core(core)
        self.validate_core(core)
        self.validate_core_id(id)
        core.set_processor(self)
        self.__cores[id] = core
        core.set_id(id)

    def get_core(self, by=None):
        """Return :class:`Processor.Core` by `by`. If `by` wasn't provided,
        return core with ID 0.
        """
        if not by:
            by = 0
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
        example for
        :class:`bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A`
        processor we are always waiting for
        :class:`bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A.Core`
        core. By default it simply reuses :func:`is_core`
        function."""
        return self.verify_core(core) #is_core(core)

    @validate(id_=int)
    def validate_core_id(self, id_):
        """Validates core `id_`, which has to be less than the total number of
        cores and greater or equal to zero.
        """
        if id_ >= 0 and self.get_num_cores() <= id_:
            raise Exception('The %s supports up to %d cores. '
                            'You have too many: %d' %
                            (self.__class__.__name__,
                             self.get_num_cores(), id_))

    def get_cores(self):
        """Returns all the cores."""
        return self.__cores

    def get_num_cores(self):
        """Return number of cores."""
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
