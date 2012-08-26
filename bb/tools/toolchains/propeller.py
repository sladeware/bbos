#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.tools.toolchains.custom_c_toolchain import CustomCToolchain
from bb.tools.compilers import propgcc

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
