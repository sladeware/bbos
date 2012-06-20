#!/usr/bin/env python

# The purpose of the test to test catalina project in combination
# with catalina compiler on the real hardware.
# This test playing with LEDs on Propeller Demo Board.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = True
LED = 18
DELAY = 1 # in seconds
LOAD_BINARY_FLAG = True # Do we need to use loader to load the binary?

project = CatalinaProject("blinker", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('ci')
compiler.define_macro("LED", LED, c_symbol=True)
compiler.define_macro("DELAY", DELAY, c_symbol=True)

# Take the sources from the same folder
sources = list()
for filename in ("blinker.c",):
    project.add_source(os.path.join(module.get_dir(), filename))

# Build the project
project.build()

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
