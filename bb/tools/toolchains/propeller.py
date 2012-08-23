#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.lib.build.toolchains.custom_c_toolchain import CustomCToolchain
from bb.lib.build.compilers import propgcc

class PropellerToolchain(CustomCToolchain):
  def __init__(self, *args, **kargs):
    CustomCToolchain.__init__(self, compiler=propgcc.PropGCCCompiler(),
                              *args, **kargs)
    # At some point propgcc doesn't provide platform macro so we need to
    # define it manually
    self.compiler.define_macro("__linux__")
    self.compiler.define_macro("BB_HAS_STDINT_H")
    self.compiler.define_macro("printf", "__simple_printf")
    self.compiler.set_memory_model("LMM") # case insensetive
    self.compiler.set_extra_preopts(["-Os", "-Wall"])
