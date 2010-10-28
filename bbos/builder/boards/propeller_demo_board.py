"""Propeller demo board from Parallax.

The Propeller Demo Board from Parallax is a compact platform designed to
demostrate all of the various capabilities of the P8X32A processor. It
provides connections and supporting devices to demostrate video, sound,
mouse, keyboard and provides a USB interface for programming. There are
8 unused I/O pins for experimentation. There are 8 LEDs, a reset push
button, an on/off switch and a 24LC256-I/ST EEPROM for program storage.
It has a 5.000MHz replacable crystal oscillator.
"""

__copyright__ = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

from lib.bbos_board import BBOSBoard
from lib.common import *
from processors.propeller_p8x32a import *


class PropellerDemoBoard(BBOSBoard):
    def __init__(self, processes, memsize):
        processors = [PropellerP8X32A(processes, memsize)]
        BBOSBoard.__init__(self, processors)

