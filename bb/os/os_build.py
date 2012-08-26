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

def os_decomposer(os):
  """Decomposes OS instances derived from OS class."""
  return os.kernels()

os_descriptor = bb.application.get_object_descriptor(OS)
#os_descriptor.decomposer = os_decomposer

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

#os_descriptor = bb.application.get_object_descriptor(OS)
#os_descriptor.build += {
  # Propeller GCC compiler support
#  'propler' : {
#    'sources': ('kernel.c', gen_config_h)
#    }
#}
