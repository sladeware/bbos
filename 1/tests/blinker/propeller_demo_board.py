#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys

from model import blinker
from bb.os.hardware.boards import PropellerDemoBoard
from bb.builder.projects import CatalinaProject
from bb.apps.utils.dir import script_relpath, script_dir

board = PropellerDemoBoard([blinker])
project = CatalinaProject("Blinker", [blinker, script_relpath('propeller_demo_board.c')])
project.get_compiler().add_include_dir(script_dir())
project.get_compiler().add_library('ci')
project.build(verbose=True) # dry_run=True
