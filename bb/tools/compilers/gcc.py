#!/usr/bin/env python

from bb.lib.build.compilers import custom_c_compiler

class LD(custom_c_compiler.Linker):
  pass
