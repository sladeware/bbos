#!/usr/bin/env python

import os.path

from bb.builder.projects import CatalinaProject
from bb.builder.loaders import BSTLLoader
from bb.utils import module

BE_VERBOSE = True

project = CatalinaProject("blinker", verbose=BE_VERBOSE)

# Let us setup catalina compiler first
compiler = project.get_compiler()
compiler.add_include_dir(module.get_dir())
compiler.add_library('ci')
compiler.define_macro("LED", 18, c_symbol=True)

# Take the sources from the same folder
sources = [os.path.join(module.get_dir(), _) for _ in ("blinker.c",)]
project.add_sources(sources)
# Build the project
project.build()

# Setup loader to load our binary
loader = BSTLLoader(verbose=BE_VERBOSE,
                    mode=BSTLLoader.Modes.RAM_ONLY,
                    device_filename="/dev/ttyUSB0")
project.set_loader(loader)

# Load the project binary
project.load()
