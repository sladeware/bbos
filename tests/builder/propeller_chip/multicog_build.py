#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = True
LOAD_BINARY_FLAG = True # Do we need to use loader to load the binary?

project = CatalinaProject("multicog", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library("ci")
# Please, in order to use the following library, install
# bb/builder/compilers/catalina first.
compiler.add_library("multicog")
# Take the sources from the same folder
sources = list()
for filename in ("multicog.c",):
    project.add_source(os.path.join(module.get_dir(), filename))

# Build the project
project.build()
