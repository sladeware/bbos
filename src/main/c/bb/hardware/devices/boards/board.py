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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.hardware.devices import Device
from bb.hardware.devices.processors import Processor
from bb.utils import typecheck

class Board(Device):
  """Base class representing a board -- i.e. computing hardware.

  A board contains one or more processors. Each processor may or may not be the
  same, depending on the board. A board is a piece of hardware that performs
  computation within its processors. Other supporting hardware may be present on
  the board, but BB does not explicitly refer to them.
  """

  def __init__(self, elements=[], processors=[]):
    Device.__init__(self)
    self._processors = []
    if processors:
      self.add_processors(processors)
    if elements:
      self.add_elements(elements)

  def add_processors(self, processors):
    if not typecheck.is_sequence(processors):
      raise TypeError('Must be a sequence')
    for processor in processors:
      self.add_processor(processor)

  def add_element(self, element):
    if isinstance(element, Processor):
      self._processors.append(element)
    Device.add_element(self, element)

  def add_processor(self, processor):
    """Adds a new element to the device/board and start tracking it as a
    processor.
    """
    if not isinstance(processor, Processor):
      raise TypeError("'processor' must be derived from Processor class.")
    self.add_element(processor)

  def get_processors(self):
    return self._processors

class Breadboard(Board):
  """A breadboard (protoboard) is a construction base for prototyping of
  electronics.

  Because the solderless breadboard does not require soldering, it is
  reusable. This makes it easy to use for creating temporary prototypes and
  experimenting with circuit design.
  """

  DESIGNATOR_FORMAT="PROTOBOARD_%d"

  def __init__(self, *args, **kwargs):
    Board.__init__(self, *args, **kwargs)

# Make Protoboard to be an alias of Breadboard
Protoboard = Breadboard
