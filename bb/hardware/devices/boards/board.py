#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.hardware import Device

#_______________________________________________________________________________

class Breadboard(Device):
    """A breadboard (protoboard) is a construction base for
    prototyping of electronics.

    Because the solderless breadboard does not require soldering, it
    is reusable. This makes it easy to use for creating temporary
    prototypes and experimenting with circuit design."""
    def __init__(self):
        Device.__init__(self)
        self.designator_format = "PROTOBOARD_%d"

# Make Protoboard to be an alias of Breadboard
Protoboard = Breadboard

#_______________________________________________________________________________

class Board(Device):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may
    not be the same, depending on the board. A board is a piece of
    hardware that performs computation within its processors. Other
    supporting hardware may be present on the board, but BB does not
    explicitly refer to them."""

    def __init__(self):
        Device.__init__(self)
