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

"""The Parallax P8X32A Propeller chip is a multi-core architecture parallel
microcontroller with eight 32-bit RISC CPU cores.

Each of the eight 32-bit cores (called a cog) has a CPU which has access to 512
32-bit long words (2 KB) of instructions and data.
"""

__copyright__ = "Copyright (c) 2011-2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

from bb.hardware.devices.processors import Processor
from bb.hardware.devices.memory import RAM
from bb.utils.type_check import verify_list

class PropellerP8X32A(Processor):
    """Parallax Propeller P8X32A processor.

    The Parallax Propeller P8X32A family of microcontrollers contains eight cogs
    (a.k.a BBOS cores). Its system clock runs up to 80MHz.

    The processor contains 32K RAM and 32K ROM globally that all cogs share
    using a multiplexed system bus. There are 32 IO pins.
    """

    class Core(Processor.Core):
        """Parallax Propeller processor's cog core.

        A "cog" is a CPU contained within the Propeller processor. Cogs are
        designed to run independently and concurrently within the same silicon
        die. They have their own internal memory, configurable counters, video
        generators and access to I/O pins as well as the system clock. All the
        cogs in the processor share access to global resources sych as the main
        RAM/ROM, synchronization resources and specialized monitoring
        capabilities to know what the other cogs are doing.
        """

        def __str__(self):
            return "Cog#%d" % self.get_id()

    Cog = Core

    def __init__(self, mappings=[]):
        verify_list(mappings)
        cores = [self.Core() for _ in range(8)]
        for mapping in mappings:
            cores.append(self.Core(mapping))
        Processor.__init__(self, 8, cores)
        self.add_property(self.Property("name", "PROPELLER_P8X32"))
        # Define Hub RAM Memory unit (in bytes)
        self.__RAM = RAM(8192 * 32)

    @property
    def RAM(self):
        return self.__RAM

    def __str__(self):
        return "Propeller P8X32A"

# A few aliases to provide termin "cog"
PropellerP8X32A.get_cog = PropellerP8X32A.get_core
PropellerP8X32A.get_cogs = PropellerP8X32A.get_cores

class PropellerP8X32A_Q44(PropellerP8X32A):
    """The P8X32A-Q44 is most useful for prototyping in its 44-pin QFP
    package."""

    def __str__(self):
        return "Propeller P8X32A-Q44"
