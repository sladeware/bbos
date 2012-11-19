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

"""Propeller GCC (propgcc) is GCC for the Parallax Propeller Microcontroller.

How to install

Download compiler <http://code.google.com/p/propgcc/downloads/list> and read
INSTALL.txt for further instructions.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.tools.compilers.gcc import GCC
from bb.utils import typecheck

class PropGCC(GCC):
  """PropGCC is a GCC port for the Parallax Propeller P8X32A
  Microcontroller. Project page: http://code.google.com/p/propgcc/.

  Please use compiler specific method instead of direct defining compiler
  options (such as memory model) in order to escape from unexpected errors. For
  example to set `lmm` memory model use :func:`set_memory_model` instead of
  defining `-mlmm` option. Otherwise you may have conflicts between symbols in
  the main C program and symbols in the local cog C program.

  Please visit `Common GCC Options
  <http://code.google.com/p/propgcc/wiki/PropGccCompileOptions>`_ to learn more
  about Propeller specific options.
  """

  EXECUTABLE = ["propeller-elf-gcc"]

  def __init__(self, *args, **kargs):
    GCC.__init__(self, *args, **kargs)
    self._memory_model = None
    self.define_macro("__linux__")
    self.define_macro("BB_HAS_STDINT_H")
    self.define_macro("printf", "__simple_printf")
    self.set_memory_model("LMM") # case insensetive
    self.set_extra_preopts(["-Os", "-Wall"])

  def set_memory_model(self, model):
    """Set memory model (not case sensetive). Available models:

    ======= ================================================================
    Model   Description
    ======= ================================================================
    cog     Generate code for COG model. In this model the code is placed in
            cog internal memory (which has only 2K). Data is placed in hub
            memory. This is the native execution mode, but is very
            restricted because of the small code size available.
    lmm     Generate code for LMM (Large Memory Model). In this model both
            code and data are placed in hub. A small kernel runs in cog
            memory to fetch code and execute it. This is the default.
    xmm     Generate code for XMM (eXternal Memory Model). In this model
            both code and data are placed in external memory (flash or RAM);
            only the stack remains in the hub memory. A kernel is run in
            cog memory to fetch instructions and data from the external
            memory.
    xmmc    Generate code for XMMC (eXternal Memory Model - Code). In this
            model code is placed in external memory (flash or RAM) and data
            is placed in the hub. A kernel is run in cog memory to fetch
            instructions from the external memory.
    ======= ================================================================
    """
    if not typecheck.is_string(model):
      raise TypeError("Must be string.")
    self._memory_model = model.lower()

  def get_memory_model(self):
    """Return memory model. See :func:`set_memory_model`."""
    return self._memory_model

  def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
    if self.get_memory_model():
      cc_args.append("-m%s" % self.get_memory_model())
    GCC._compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts)

  def _link(self, objects, output_dir=None, libraries=None, library_dirs=None,
            debug=False, extra_preargs=None, extra_postargs=None,
            target_lang=None):
    if not extra_preargs:
      extra_preargs = []
    if self.get_memory_model():
      extra_preargs.append("-m%s" % self.get_memory_model())
    extra_preargs.extend(self.get_linker().get_opts()) # remove this!
    GCC._link(self, objects, output_dir, libraries,
              library_dirs, debug, extra_preargs,
              extra_postargs, target_lang)
