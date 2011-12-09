#!/usr/bin/env python

from bb.hardware import Part

#_______________________________________________________________________________

class Breadboard(Part):
    pass

#_______________________________________________________________________________

class Board(Part):
    """Base class representing a board -- i.e. computing hardware.

    A board contains one or more processors. Each processor may or may
    not be the same, depending on the board. A board is a piece of
    hardware that performs computation within its processors. Other
    supporting hardware may be present on the board, but BB does not
    explicitly refer to them."""

    def __init__(self, name):
        Part.__init__(self, name)

