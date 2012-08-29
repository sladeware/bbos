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

import bb
from bb.os import OS
from bb.tools.generators import CGenerator

with OS as bundle:
  def dependency_resolver(self, os):
    """Decomposes OS instances derived from OS class."""
    return [os.get_processor()] + os.get_kernels()
  bundle.decomposer = dependency_resolver

# TODO(team): the following code has to be moved with all C files, once C
# implementation will be separated.

def gen_config_h(os):
  file_path = bb.host_os.path.join(bb.env.pwd(), 'config_autogen.h')
  g = CGenerator().create(file_path)
  for kernel in os.get_kernels():
    for i in range(kernel.get_num_threads()):
      thread = kernel.get_threads()[i]
      g.writeln("#define %s %d" % (thread.get_name(), i))
      g.writeln("#define %s_RUNNER %s" % (thread.get_name(),
                                          thread.get_runner()))
  g.close()

with OS as bundle:
  bundle.build_cases.update({
    # Propeller GCC compiler support
    'propeller' : {
      'sources': (gen_config_h,)
      }
    })
