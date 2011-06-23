#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys

from model import blinker
from bb.os.hardware.boards import PropellerDemoBoard
from bb.builder.projects import CatalinaProject

board = PropellerDemoBoard([blinker])
project = CatalinaProject("Blinker")





