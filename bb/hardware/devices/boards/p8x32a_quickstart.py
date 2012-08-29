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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.hardware.devices.boards.board import Board
from bb.hardware.devices.processors import PropellerP8X32A
from bb.hardware.devices.leds import LED
from bb.hardware.devices.gpio import Button

class P8X32A_QuickStartBoard(Board):
  """This class represents `P8X32A QuickStart board
  <http://www.parallax.com/StoreSearchResults/tabid/768/txtSearch/QuickStart/List/0/SortField/4/ProductID/748/Default.aspx>`_.

  Please see http://www.parallaxsemiconductor.com/sites/default/files/parallax/P8X32AQuickStartSchematicRevA_2.pdf
  for schematic.
  """

  PROPERTIES = (Board.Property('name', 'P8X32A QuickStartBoard'),)

  def __init__(self):
    Board.__init__(self)
    # TODO(team): fix the problem with processors
    self.add_processor(PropellerP8X32A().set_designator('U1'))
    # Add LED's
    self.add_elements([LED().set_designator("D%d" % i) for i in range(1, 9)])
    self.add_elements([Button().set_designator("B%d" % i) for i in range(1, 9)])
