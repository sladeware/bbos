# -*- coding: utf-8; mode: python; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC

import os

def require(spec):
  from bb.tools.b3 import buildfile
  ctx = buildfile.Context.locate()
  address = buildfile.get_address(ctx.buildfile.root_dir, spec, False)
  if not address:
    return None
  return buildfile.Context(address.buildfile).parse()

# Load BUILD files for each language from main, e.g. c, dynamic_c, etc.
# This will add new rules and primitives that will expand current state.
subdirs = filter(os.path.isdir, os.listdir(os.path.dirname(__file__)))
for subdir in subdirs:
  require(os.path.join(subdir, "bb", "os"))

# FIXME:
require(os.path.join(os.path.dirname(__file__), "c", "bb", "os", "drivers",
                     "processors", "propeller_p8x32"))
require(os.path.join(os.path.dirname(__file__), "c", "bb", "os", "drivers",
                     "gpio"))
