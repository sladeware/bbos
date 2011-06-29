#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import module

from model import blinker
from bb.os.hardware.boards import PropellerDemoBoard
from bb.builder.projects import CatalinaProject

board = PropellerDemoBoard([blinker])
project = CatalinaProject("Blinker", [blinker])
for source_file in ('propeller_demo_board.c',):
    project.add_source(module.get_file(__name__, source_file))
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('ci')
compiler.define_macro("LED", 18)
project.build(verbose=False, dry_run=False)
