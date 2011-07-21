#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import module

from bb import app
from bb.builder.projects import CatalinaProject

from application import blinker

project = CatalinaProject("Blinker", [blinker])
for source_file in ('blinker.c',):
	project.add_source(module.get_file(__name__, source_file))

# Setup compiler
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('ci')
compiler.define_macro("LED", 18)

# Build application
project.build(verbose=False, dry_run=False)


