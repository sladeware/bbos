# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
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
#
# Author: Oleksandr Sviridenko

from bb.utils.testing import unittest
from bb.tools.compilers.compiler import Compiler

class CompilerTest(unittest.TestCase):

  def test_dry_run_mode(self):
    compiler = Compiler(dry_run=True)
    self.assert_true(compiler.is_dry_run_mode_enabled())

  def test_sources(self):
    srcs = ["compiler.py", "propgcc.py"]
    compiler = Compiler(files=srcs)
    self.assert_equal(len(srcs), len(compiler.get_files()))
    def gen_sources():
      return ["cc.py", "python.py"]
    compiler.add_file(gen_sources)
    self.assert_equal(len(compiler.get_files()), len(srcs) + len(gen_sources()))
