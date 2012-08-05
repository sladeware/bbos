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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.lib.build.compilers.custom_c_compiler import CustomCCompiler
from bb.lib.build.compilers.gcc import LD
from bb.lib.utils import spawn
from bb.lib.utils.host_os.path import mkpath
from bb.config import host_os

class UnixCCompiler(CustomCCompiler):
  """This class is subclass of
  :class:`bb.lib.build.compilers.custom_c_compiler.CCompiler` that handles the
  typical Unix-style command-line C compiler.

  * macros defined with `-Dname[=value]`
  * macros undefined with `-Uname`
  * include search directories specified with `-Idir`
  * libraries specified with `-llib`
  * library search directories specified with `-Ldir`
  * compile handled by **cc** (or similar) executable with `-c` option:
    compiles ``.c`` to ``.o``
  * link static library handled by **ar** command (possibly with **ranlib**)
  * link shared library handled by **cc** `-shared`
  """

  SOURCE_EXTENSIONS = ['.c', '.C', '.cc', '.cxx', '.cpp', '.m']
  """Default source extensions are ``.c``, ``.C``, ``.cc``, ``.cxx``,
  ``.cpp``, ``.m``.
  """

  OBJECT_EXTENSION = ".o"
  EXECUTABLES = {
    'preprocessor' : None,
    'compiler'     : ["cc"],
    'compiler_so'  : ["cc"],
    'compiler_cxx' : ["cc"],
    'linker_so'    : ["cc", "-shared"],
    'linker_exe'   : ["cc"],
    'archiver'     : ["ar", "-cr"],
    'ranlib'       : None,
    }
  """Unix compiler specific executables:

  ============  ================
  Name          Command
  ============  ================
  preprocessor  None
  compiler      **cc**
  compiler_so   **cc**
  compiler_cxx  **cc**
  linker_so     **cc** `-shared`
  linker_exe    **cc**
  archiver      **ar** `-cr`
  ranlib        None
  ============  ================
  """

  def __init__(self, verbose=None, dry_run=False):
    CustomCCompiler.__init__(self, verbose, dry_run)
    for name, executable in UnixCCompiler.EXECUTABLES.items():
      if not self.get_executable(name):
        self.set_executable(name, executable)
    self.set_linker(LD())

  def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
    compiler = self.get_executable('compiler')
    try:
      spawn.spawn(compiler + cc_args + [src, '-o', obj] + extra_postargs,
                  debug=self.verbose, dry_run=self.dry_run)
    except spawn.ExecutionError, msg:
      raise Exception(msg) # CompileError

  def _link(self, objects, output_dir=None, libraries=None, library_dirs=None,
              debug=False, extra_preargs=None, extra_postargs=None,
              target_lang=None):
    """Linking."""
    objects, output_dir, libraries, library_dirs = \
        self._setup_link(objects, output_dir, libraries, library_dirs)
    lib_options = self._gen_lib_options(library_dirs, libraries)
    # Finalize linker options
    ld_options = self._gen_ld_options(debug, extra_preargs)
    if extra_postargs:
      ld_options.extend(extra_postargs)
    ld_options += (objects + lib_options + ['-o', self.get_output_filename()])
    mkpath(host_os.path.dirname(self.get_output_filename()))
    try:
      linker = self.get_executable("linker_exe")
      # TODO: fix this
      target_lang = "c++"
      if target_lang == "c++" and self.get_executable("compiler_cxx"):
        # skip over environment variable settings if /usr/bin/env is used to set
        # up the linker's environment. This is needed on OSX. Note: this
        # assumes that the normal and C++ compiler have the same environment
        # settings.
        i = 0
        if host_os.path.basename(linker[0]) == "env":
          i = 1
          while '=' in linker[i]:
            i = i + 1
        # TODO: resolve this
        #linker[i] = self.get_executable('compiler_cxx')[i]
        spawn.spawn(linker + ld_options, debug=self.verbose, \
                dry_run=self.dry_run)
    except Exception, msg:
      raise Exception, msg

  def get_library_option(self, lib):
    return "-l" + lib
