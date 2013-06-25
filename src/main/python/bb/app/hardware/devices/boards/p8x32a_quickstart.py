#!/usr/bin/env python
#
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

from bb.app.hardware.devices.boards.board import Board
from bb.app.hardware.devices.processors import PropellerP8X32A
from bb.app.hardware.devices.leds import LED
from bb.app.hardware.devices.gpio import Button

class P8X32A_QuickStartBoard(Board):
  """This class represents `P8X32A QuickStart board <http://goo.gl/9808F>`_.

  Please see <http://goo.gl/39ZJk> for schematic.
  """

  PROPERTIES = (("name", "P8X32A QuickStartBoard"),)

  def __init__(self):
    Board.__init__(self)
    self.add_processor(PropellerP8X32A().set_designator("U1"))
    # Add LED's and button's
    self.add_elements([LED().set_designator("D%d" % i) for i in range(1, 9)])
    self.add_elements([Button().set_designator("B%d" % i) for i in range(1, 9)])

  def get_processor(self):
    """P8X32A QuickStartBoard has only one processor. Returns this processor.

    :returns: An :class:`~bb.app.hardware.devices.processors.propeller_p8x32.PropellerP8X32A` instance.
    """
    return self.get_processors()[0]
