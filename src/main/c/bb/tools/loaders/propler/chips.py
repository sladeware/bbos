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
__all__ = ["PropellerP8X32"]

class PropellerP8X32(object):
  """This class represents Parallax P8X32A Propeller chip with a
  multi-core architecture parallel microcontroller with eight
  32-bit RISC CPU cores.Propeller chip.
  """

  NR_COGS = 8
  RAM_SIZE = 262144

  class ClockModes:
    """Valid Clock Modes.

    =============  =====
    Mode           Value
    =============  =====
    RCFASE         0x00
    RCSLOW         0x01
    XINPUT         0x22
    XTAL1          0x2A
    XTAL2          0x32
    XTAL3          0x3A
    XINPUT_PLL1X   0x63
    XINPUT_PLL2X   0x64
    XINPUT_PLL4X   0x65
    XINPUT_PLL8X   0x66
    XINPUT_PLL16X  0x67
    XTAL1_PLL1X    0x6B
    XTAL1_PLL2X    0x6C
    XTAL1_PLL4X    0x6D
    XTAL1_PLL8X    0x6E
    XTAL1_PLL16X   0x6F
    XTAL2_PLL1X    0x73
    XTAL2_PLL2X    0x74
    XTAL2_PLL4X    0x75
    XTAL2_PLL8X    0x76
    XTAL2_PLL16X   0x77
    XTAL3_PLL1X    0x7B
    XTAL3_PLL2X    0x7C
    XTAL3_PLL4X    0x7D
    XTAL3_PLL8X    0x7E
    XTAL3_PLL16X   0x7F
    =============  =====
    """
    RCFASE        = 0x00
    RCSLOW        = 0x01
    XINPUT        = 0x22
    XTAL1         = 0x2A
    XTAL2         = 0x32
    XTAL3         = 0x3A
    XINPUT_PLL1X  = 0x63
    XINPUT_PLL2X  = 0x64
    XINPUT_PLL4X  = 0x65
    XINPUT_PLL8X  = 0x66
    XINPUT_PLL16X = 0x67
    XTAL1_PLL1X   = 0x6B
    XTAL1_PLL2X   = 0x6C
    XTAL1_PLL4X   = 0x6D
    XTAL1_PLL8X   = 0x6E
    XTAL1_PLL16X  = 0x6F
    XTAL2_PLL1X   = 0x73
    XTAL2_PLL2X   = 0x74
    XTAL2_PLL4X   = 0x75
    XTAL2_PLL8X   = 0x76
    XTAL2_PLL16X  = 0x77
    XTAL3_PLL1X   = 0x7B
    XTAL3_PLL2X   = 0x7C
    XTAL3_PLL4X   = 0x7D
    XTAL3_PLL8X   = 0x7E
    XTAL3_PLL16X  = 0x7F

    to_string = {
      XTAL1         : "XTAL1",
      XTAL2         : "XTAL1",
      XTAL3         : "XTAL1",
      XINPUT_PLL1X  : "XINPUT_PLL1X",
      XINPUT_PLL2X  : "XINPUT_PLL2X",
      XINPUT_PLL4X  : "XINPUT_PLL4X",
      XINPUT_PLL8X  : "XINPUT_PLL8X",
      XINPUT_PLL16X : "XINPUT_PLL16X",
      XTAL1_PLL1X   : "XTAL1_PLL1X",
      XTAL1_PLL2X   : "XTAL1_PLL2X",
      XTAL1_PLL4X   : "XTAL1_PLL4X",
      XTAL1_PLL8X   : "XTAL1_PLL8X",
      XTAL1_PLL16X  : "XTAL1_PLL16X",
      XTAL2_PLL1X   : "XTAL2_PLL1X",
      XTAL2_PLL2X   : "XTAL2_PLL2X",
      XTAL2_PLL4X   : "XTAL2_PLL4X",
      XTAL2_PLL8X   : "XTAL2_PLL8X",
      XTAL2_PLL16X  : "XTAL2_PLL16X",
      XTAL3_PLL1X   : "XTAL3_PLL1X",
      XTAL3_PLL2X   : "XTAL3_PLL2X",
      XTAL3_PLL4X   : "XTAL3_PLL4X",
      XTAL3_PLL8X   : "XTAL3_PLL8X",
      XTAL3_PLL16X  : "XTAL3_PLL16X"
      }
    """Convert clock mode value to string."""
