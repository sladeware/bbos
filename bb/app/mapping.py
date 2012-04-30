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

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"

#_______________________________________________________________________________

from bb.hardware import Device
from bb.hardware.devices.boards import Board
from bb.hardware.devices.processors import Processor

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
        if not self.get_processor():
            return None
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
    """The mapping describes a particular CPU core and the particular
    operating system kernel on it. It represents the life of that kernel: from
    its initialization to the point that it stops executing."""
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
