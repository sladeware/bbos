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

Suppose you would like to create a new army of robots. Each robot will have
name of format ``ROBOT%d`` and will be powered by operating system ``RobotOS``.
Several ways to define a new :class:`Mapping` that will control our robot::

    class Robot(Mapping):
        NAME_FORMAT="ROBOT%d"
        OS_CLASS=RobotOS

or with help of :func:`mapping_factory` factory::

    robot_class = mapping_factory(name_format="ROBOT%d", os_class=RobotOS)

Once the class has been created we can create our first robot::

    robot1 = robot_class()

Once the mapping is created it has to bind to hardware. The role of bridge
between :class:`Mapping` and hardware plays :class:`HardwareAgent`. Let us
assume that our robot device described by ``device``, which has a board with
designator ``BRD1`` and processor ``PRCR1`` on it. Now we need to find the
:class:`bb.hardware.devices.processors.processor.Processor.Core` and connect it
to the :class:`Mapping`::

    board = device.find_element("BRD1")
    processor = board.find_element("PRCR1")
    core = processor.get_core() # get core #0
    core.set_mapping(robot1)

Now we can explore hardware, for example print the processor's short
description::

    print robot1.hardware.get_processor()

"""

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"
__author__ = "Alexander Sviridenko"

from bb.hardware import Device
from bb.hardware.devices.boards import Board
from bb.hardware.devices.processors import Processor
from bb.utils.instance import InstanceTracking

class HardwareAgent(object):
    """This class represents an agent that provides an interface between a
    single mapping and hardware abstraction. Only the agent knows where the
    mapping lives.

    For example on which core of which processor and on what
    board.

    """

    def __init__(self, core=None):
        self.__core = None
        if core:
            self.set_core(core)

    def is_board_defined(self):
        """Return whether or not the agent can identify the board."""
        return not not self.get_board()

    def get_board(self):
        """Return :class:`bb.hardware.devices.boards.board.Board` instance on
        which :class:`bb.hardware.devices.processors.processor.Processor` is
        located.
        """
        processor = self.get_processor()
        if not processor:
            return None
        board = None
        for neighbour in processor.get_neighbours():
            if isinstance(neighbour, Board):
                board = neighbour
        if not board:
            raise
        return board

    def is_processor_defined(self):
        """Whether or not a processor was defined. Return ``True`` value if the
        :class:`bb.hardware.devices.processors.processor.Processor` instance
        can be obtained by using specified core. Otherwise return ``False``."""
        return not not self.get_processor()

    def get_processor(self):
        """Return :class:`bb.hardware.devices.processors.processor.Processor`
        instance."""
        if not self.get_core():
            return None
        return self.get_core().get_processor()

    def is_core_defined(self):
        """Whether or not a core was defined."""
        return not not self.get_core()

    def set_core(self, core):
        """Set :class:`bb.hardware.devices.processors.processor.Processor.Core`
        instance."""
        if not isinstance(core, Processor.Core):
            raise TypeError("Core must be %s sub-class" %
                            Processor.Core.__class__.__name__)
        self.__core = core

    def get_core(self):
        """Return
        :class:`bb.hardware.devices.processors.processor.Processor.Core`
        instance."""
        return self.__core

class Mapping(InstanceTracking):
    """:class:`Mapping` describes a particular CPU core and the particular
    operating system kernel on it. It represents the life of that kernel: from
    its initialization to the point that it stops executing.

    The following example shows a simple way to use mapping::

        robot = Mapping("Robot", os_class=RobotOS)

    This class also inhertis :class:`bb.utils.instance.InstanceTracking` class
    in order to track all created instances."""

    OS_CLASS=None
    """This constant defines operating system class that will be used by
    default by the mapping. By default mapping will use
    :class:`bb.os.kernel.OS` class."""

    NAME_FORMAT="M%d"
    """Default name format is using in order to automatically generate
    mapping name. Usually mappings of the same class have the same nature and
    so no reason to invent a new name for each mapping. By default the 
    format has view ``M%d`` and based on the number of mappings in the
    application (see :func:`bb.app.application.Application.get_num_mappings`).

    """

    HARDWARE_AGENT_CLASS=HardwareAgent
    """Hardware agent class that is the bridge between hardware and process."""

    def __init__(self, name=None, name_format=None,
                 os_class=None,
                 hardware_agent_class=None,
                 build_params=None):
        # Initialize sub-classes
        InstanceTracking.__init__(self)
        # Define mapping name format
        self.__name_format = name_format
        self.set_name_format(self.NAME_FORMAT)
        if name_format:
            self.set_name_format(name_format)
        self.__name = None
        # Define mapping name or generate it
        if name:
            self.set_name(name)
        else:
            self.gen_name()
        # Build params
        self.__build_params = dict()
        if build_params:
            self.set_build_params(build_params)
        # Hardware agent
        if not hardware_agent_class:
            hardware_agent_class = self.HARDWARE_AGENT_CLASS
        self.__hardware_agent = hardware_agent_class()
        # Operating system
        self.__os_class = None
        self.set_os_class(self.OS_CLASS)
        if os_class:
            self.set_os_class(os_class)

    def set_build_params(self, build_params):
        """Set `build_params` as built-time parameters."""
        self.__build_params = build_params

    def get_build_params(self):
        """Return dictionary of build params."""
        return self.__build_params

    def set_os_class(self, os_class):
        """Set `os_class` derived from :class:`bb.os.kernel.OS` class as
        operating system class that will be instantiated by this mapping."""
        self.__os_class = os_class

    def get_os_class(self):
        """Return operating system class that will control the future system."""
        return self.__os_class

    @property
    def hardware(self):
        """An alias for :func:`get_hardware_agent`."""
        return self.get_hardware_agent()

    def get_hardware_agent(self):
        """Return hardware agent instance. The agent should be derived from
        :class:`HardwareAgent` class."""
        return self.__hardware_agent

    def set_name_format(self, frmt):
        self.__name_format = frmt

    def get_name_format(self):
        """Return name format."""
        return self.__name_format

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

           The name must be unique within an application.
        """
        self.__name = name

    def get_name(self):
        return self.__name

    def __str__(self):
        return "Mapping %s" % self.get_name()

def mapping_factory(*args, **kargs):
    """:class:`Mapping` factory. Return new class derived from
    :class:`Mapping` class."""
    class MappingContainer(Mapping):
        def __init__(self):
            Mapping.__init__(self, *args, **kargs)
    return MappingContainer

def verify_mapping(mapping):
    if not isinstance(mapping, Mapping):
        raise TypeError("Unknown mapping '%s'. "
                        "Not a subclass of bb.mapping.Mapping class" %
                        (mapping))
    return mapping
