#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import module

from bb import app
from bb.builder.projects import CatalinaProject

from accel import accel

project = CatalinaProject("Accel", [accel])
for source_file in ('accel.c',):
	project.add_source(module.get_file(__name__, source_file))

# Setup compiler
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('ci')
compiler.define_macro('DEMO')
compiler.define_macro('PC')

# Loader
from bb.builder.loaders import BSTLLoader
project.set_loader(BSTLLoader())

# Build application
project.build(verbose=True, dry_run=False)

project.load()

