#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = False
LOAD_BINARY_FLAG = True # Do we need to use loader to load the binary?

project = CatalinaProject("ping", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dirs(["./../../..", "."])

# Add required libraries
compiler.add_library("ci")
# Please, in order to use the following library, install
# bb/builder/compilers/catalina first.
compiler.add_library("multicog")

# Add sources
for filename in ("./../../../bb/os.c", "./../../../bb/os/kernel.c",
                 "./../../../bb/os/kernel/itc.c", "./../../../bb/mm/mempool.c",
                 "./../../../bb/os/kernel/schedulers/fcfsscheduler.c"):
  project.add_source(filename)
# Take the sources from the same folder
for filename in ("ping.c",):
    project.add_source(os.path.join(module.get_dir(), filename))

# Build the project
project.build()
