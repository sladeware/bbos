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

"""Propeller demo board from Parallax."""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.hardware.devices.boards import Board, Breadboard
from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A

class PropellerDemoBoard(Board):
  """Propeller Demo Board base class derived from
  :class:`bb.hardware.devices.boards.board.Board` class.

  The Propeller Demo Board from Parallax is a compact platform designed to
  demostrate all of the various capabilities of the P8X32A processor. It
  provides connections and supporting devices to demostrate video, sound, mouse,
  keyboard and provides a USB interface for programming. There are 8 unused I/O
  pins for experimentation. There are 8 LEDs, a reset push button, an on/off
  switch and a 24LC256-I/ST EEPROM for program storage.  It has a 5.000MHz
  replacable crystal oscillator.
  """

  def __init__(self):
    Board.__init__(self)
    self.add_elements(PropellerP8X32A(), Breadboard())
