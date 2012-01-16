#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = True
LOAD_BINARY_FLAG = True # Do we need to use loader to load the binary?

project = CatalinaProject("vegimeter", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dirs(["./../..", "."])

# Add required libraries
compiler.add_library("ci")
# You need to execute make in bb/builder/compilers/catalina to use this
compiler.add_library("multicog")

# Add sources
for filename in ("./../../bb/os.c",
                 "./../../bb/os/kernel.c",
                 "./../../bb/os/kernel/schedulers/fcfsscheduler.c"):
  project.add_source(filename)
for filename in ("temp_sensor_driver_soil_a.c",):
    project.add_source(os.path.join(module.get_dir(), filename))

# Add source files
filename = "temp_sensor_driver_soil_a.c"
project.add_source(os.path.join(module.get_dir(), filename))

# Build the project
project.build(verbose=BE_VERBOSE)

# Skip the last part if we do not need to load binary
if not LOAD_BINARY_FLAG:
    exit(0)

# Setup loader to load our binary
loader = BSTLLoader(verbose=BE_VERBOSE,
                    mode=BSTLLoader.Modes.RAM_ONLY,
                    device_filename="/dev/ttyUSB0")
project.set_loader(loader)

# Load the project binary
project.load()
