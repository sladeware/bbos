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

"""The mapping of hardware resources to software runtime components such as
processes, threads, queues and pools is determined at compile time. Thereby
permitting system integrators to cleanly separate the concept of what the
software does and where it does it.

Compile time mapping is critical for tuning a system based on application
requirements. It is useful when faced with an existing software application
that must run on a new or updated hardware platform, thus requiring
re-tuning of the application. Equally important is the flexibility afforded
by compile time mapping to system integrators that need to incorporate new
software features as applications inevitably grow in complexity.
"""

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"
__author__ = "Alexander Sviridenko <oleks.sviridenko@gmail.com>"

from bb.hardware.devices.processors import Processor

class HardwareConnector(object):
    """This class represents a connector that provides an interface between a
    single mapping and hardware abstraction.
    """

    def __init__(self, processor=None):
        self._processor = None
        self._is_simulation_mode = False
        if processor:
            if not isinstance(processor, Processor):
                raise TypeError("Processor must be %s sub-class" %
                                Processor.__class__.__name__)
            self.set_processor(processor)

    def set_simulation_mode(self):
        self._is_simulation_mode = True

    def is_simulation_mode(self):
        return self._is_simulation_mode

    def is_processor_defined(self):
        """Whether or not a processor was defined. Return ``True`` value if the
        :class:`bb.hardware.devices.processors.processor.Processor` instance can
        be obtained by using specified core. Otherwise return ``False``.
        """
        return not not self.get_processor()

    def get_processor(self):
        """Return :class:`bb.hardware.devices.processors.processor.Processor`
        instance.
        """
        return self._processor

    def set_processor(self, processor):
        """Set :class:`bb.hardware.devices.processors.processor.Processor`
        instance."""
        if not isinstance(processor, Processor):
            raise TypeError("Processor must be %s sub-class" %
                            Processor.__class__.__name__)
        self._processor = processor


class Autonaming(object):
    NAME_FORMAT="O%d"

    def __init__(self, name=None, name_format=None):
        self._name = None
        self._name_format = None
        self.set_name_format(self.NAME_FORMAT)
        if name_format:
            self.set_name_format(name_format)
        if name:
            self.set_name(name)
        else:
            self.gen_name()

    def set_name_format(self, frmt):
        self._name_format = frmt

    def get_name_format(self):
        """Return name format."""
        return self._name_format

    def gen_name(self):
        """Generate unique name for this mapping. Generator uses name format
        (see :func:`get_name_format`) and number of instances
        (see :func:`bb.utils.instance.InstanceTracking.get_num_instances`) of
        the particular :class:`Mapping` class.
        """
        frmt = self.get_name_format()
        self.set_name(frmt % self.get_num_instances())
        return self.get_name()

    def set_name(self, name):
        """Set mapping name.

        .. note::

           The name must be unique within an application network.
        """
        self._name = name

    def get_name(self):
        """Return name."""
        return self._name

class Mapping(object):
    """:class:`Mapping` describes a particular CPU and the particular
    microkernels on it. It represents the life of that microkernel:
    from its initialization to the point that it stops executing.
    """

    NAME_FORMAT = "M%d"
    """Default name format is using in order to automatically generate mapping
    name. Usually mappings of the same class have the same nature and so no
    reason to invent a new name for each mapping. By default the format has view
    ``M%d`` and based on the number of mappings in the application (see
    :func:`bb.app.Application.get_num_mappings`).
    """

    HARDWARE_CONNECTOR_CLASS = HardwareConnector
    """Hardware connector class that is the bridge between hardware and process."""

    def __init__(self, name=None, name_format=None, hardware_connector_class=None,
                 build_params=None):
        InstanceTracking.__init__(self)
        Autonaming.__init__(name, name_format)
        self._threads = list()
        self._hardware_connector = None
        if not hardware_connector_class:
            hardware_connector_class = self.HARDWARE_CONNECTOR_CLASS
        self._hardware_connector = hardware_connector_class()

    def register_thread(self, thread):
        self._threads.append(thread)
        return thread

    def register_threads(self, threads):
        for thread in threads:
            self.register_thread(thread)

    def get_threads(self):
        return self._threads

    @property
    def hardware(self):
        """An alias for :func:`get_hardware_connector`."""
        return self.get_hardware_connector()

    def get_hardware_connector(self):
        """Return hardware agent instance. The agent should be derived from
        :class:`HardwareAgent` class.
        """
        return self.__hardware_connector

    def __str__(self):
        return "Mapping %s" % self.get_name()

