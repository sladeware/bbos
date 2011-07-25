#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

"""Propeller demo board from Parallax.

The Propeller Demo Board from Parallax is a compact platform designed to
demostrate all of the various capabilities of the P8X32A processor. It
provides connections and supporting devices to demostrate video, sound,
mouse, keyboard and provides a USB interface for programming. There are
8 unused I/O pins for experimentation. There are 8 LEDs, a reset push
button, an on/off switch and a 24LC256-I/ST EEPROM for program storage.
It has a 5.000MHz replacable crystal oscillator."""

from bb.os.hardware import Board
from bb.os.hardware.processors import PropellerP8X32A

class PropellerDemoBoard(Board):
    """Propeller Demo Board base class."""
    def __init__(self, processes):
        processors = [PropellerP8X32A(processes)]
        Board.__init__(self, "Propeller Demo Board", 1, processors)

