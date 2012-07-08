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

import os

from bb.builder.compilers import new_ccompiler
from bb.builder.toolchains.toolchain import Toolchain

class CToolchain(Toolchain):
    """C toolchain for C-like compilers."""
    def __init__(self, sources=[], version=None, verbose=None, compiler=None,
                 loader=None):
        Toolchain.__init__(self, sources, version, verbose, compiler, loader)
        # Set the compiler if such was not defined
        if not self.compiler:
            self.compiler = new_ccompiler()

    def get_output_filename(self):
        """Return output file name."""
        return self.compiler.get_output_filename()

    def _build(self, sources, include_dirs=[], macros=[], libraries=[],
               library_dirs=[], dry_run=False):
        self.output_filepath = os.path.join(self.compiler.get_output_dir(), \
                                                self.compiler.get_output_filename())
        built_objects = self.compiler.compile(sources,
                                              include_dirs=include_dirs,
                                              macros=macros)
        self.compiler.link(built_objects, self.output_filepath,
                           libraries=libraries,
                           library_dirs=library_dirs)

    def load(self):
        pass # pass it for simulation
