#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys

from bb.builder import script
from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader

import module

from blinker import blinker

project = CatalinaProject("Blinker", [blinker])
for source_file in ('blinker.c',):
    project.add_source(module.get_file(__name__, source_file))

# Setup compiler
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('c')
compiler.define_macro("SMALL")
compiler.define_macro("LED", 18, c_symbol=True)

# Build application
project.build(verbose=False, dry_run=script.config.options.dry_run)

# Loader
if script.config.options.autoload:
    project.set_loader(BSTLLoader())
    project.load()

