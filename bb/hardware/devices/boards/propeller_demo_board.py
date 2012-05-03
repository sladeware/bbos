#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

"""Propeller demo board from Parallax."""

from bb.hardware.devices.boards import Board, Breadboard
from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A

#_______________________________________________________________________________

class PropellerDemoBoard(Board):
    """Propeller Demo Board base class derived from
    :class:`bb.hardware.devices.boards.board.Board` class.

    The Propeller Demo Board from Parallax is a compact platform designed to
    demostrate all of the various capabilities of the P8X32A processor. It
    provides connections and supporting devices to demostrate video, sound,
    mouse, keyboard and provides a USB interface for programming. There are 8
    unused I/O pins for experimentation. There are 8 LEDs, a reset push button,
    an on/off switch and a 24LC256-I/ST EEPROM for program storage.  It has a
    5.000MHz replacable crystal oscillator."""

    def __init__(self):
        Board.__init__(self)
        self.metadata.name = "Propeller Demo Board"
        processor = PropellerP8X32A()
        self.add_part(processor)
        protoboard = Breadboard()
        self.add_part(protoboard)

