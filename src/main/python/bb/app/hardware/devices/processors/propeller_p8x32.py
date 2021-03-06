# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

"""The Parallax P8X32A Propeller chip is a multi-core architecture parallel
microcontroller with eight 32-bit RISC CPU cores.

Each of the eight 32-bit cores (called a cog) has a CPU which has access to 512
32-bit long words (2 KB) of instructions and data.
"""

from processor import Processor, Core
from bb.utils import typecheck

class PropellerCore(Core):
  """This class represents Parallax Propeller processor's core/cog.

  A `cog` is a CPU contained within the Propeller processor. Cogs are designed
  to run independently and concurrently within the same silicon die. They have
  their own internal memory, configurable counters, video generators and access
  to I/O pins as well as the system clock. All the cogs in the processor share
  access to global resources sych as the main RAM/ROM, synchronization resources
  and specialized monitoring capabilities to know what the other cogs are doing.
  """

  def __init__(self, *args, **kwargs):
    Core.__init__(self, *args, **kwargs)

  def __str__(self):
    return "Cog[i=%d]" % self.get_id()

PropellerCog = PropellerCore

class PropellerP8X32A(Processor):
  """This class represents Parallax Propeller P8X32A processor.

  The Parallax Propeller P8X32A family of microcontrollers contains eight cogs
  (a.k.a BBOS cores). Its system clock runs up to 80MHz.

  The processor contains 32K RAM and 32K ROM globally that all cogs share using
  a multiplexed system bus. There are 32 IO pins.
  """

  core_class = PropellerCog
  default_properties = (("name", "Propeller P8X32A"),
                        ("family", "propeller_p8x32"))

  def __init__(self):
    cores = list()
    cores = [PropellerCog(self, id_=_) for _ in range(8)]
    Processor.__init__(self, 8, cores)

  def __str__(self):
    return "%s[num_cogs=%d]" % (self.__class__.__name__, self.get_num_cores())

# A few aliases for the new "cog" teminalogy
PropellerP8X32A.get_cog = PropellerP8X32A.get_core
PropellerP8X32A.get_cogs = PropellerP8X32A.get_cores

class PropellerP8X32A_Q44(PropellerP8X32A):
  """The P8X32A-Q44 is most useful for prototyping in its 44-pin QFP package.
  """

  default_properties = (("name", "Propeller P8X32A-Q44"),)
