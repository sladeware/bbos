#!/usr/bin/env python

from bb.builder.toolchains.c import CToolchain
from bb.builder.compilers import PropGCCCompiler
from bb.builder import toolchain_manager

@toolchain_manager.toolchain
class PropGCCToolchain(CToolchain):
    def __init__(self, *arglist, **argdict):
        CToolchain.__init__(self, compiler=PropGCCCompiler(), *arglist, **argdict)
        # At some point propgcc doesn't provide platform macro so we need to
        # define it manually
        self.compiler.define_macro("__linux__")
        self.compiler.define_macro("BB_HAS_STDINT_H")
        self.compiler.define_macro("printf", "__simple_printf")
        self.compiler.set_memory_model("LMM") # case insensetive
        self.compiler.set_extra_preopts(["-Os", "-Wall"])
