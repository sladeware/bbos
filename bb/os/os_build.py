#!/usr/bin/env python
#
# Copyright (c) 2012 Sladeware LLC
# http://www.bionicbunny.org/
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

def gen_os_c(os):
  file_path = bb.host_os.path.join(bb.env.pwd(), '..', 'os_autogen.c')
  g = CGenerator().create(file_path)
  g.writeln('#include "os.h"')
  g.writeln()
  for i, thread in enumerate(os.get_threads()):
    if not thread.get_num_ports():
      continue
    for j, port in enumerate(thread.get_ports()):
      g.writeln('MEMPOOL_PARTITION(thread%d_port%d_part, %d, %s);' % \
                  (i, j, port.get_capacity(), 'BBOS_MAX_MESSAGE_SIZE'))
  g.writeln()
  g.writeln('bbos_thread_t bbos_threads[BBOS_NR_THREADS] = {')
  for i, thread in enumerate(os.get_threads()):
    g.writeln('  {%s, %s},' % (thread.get_runner(), 'NULL'))
  g.writeln('};')
  g.writeln()
  g.writeln('void')
  g.writeln('bbos_init()')
  g.writeln('{')
  for i, thread in enumerate(os.get_threads()):
    if not thread.get_num_ports():
      continue
    for j, port in enumerate(thread.get_ports()):
      v = 'thread%d_port%d' % (i, j)
      g.writeln('  bbos_port_t %s = mempool_init(%s_part, %d, %s);' % \
                  (v, v, port.get_capacity(), 'BBOS_MAX_MESSAGE_SIZE'))
      g.writeln('  bbos_threads[%d].default_port = %s;' % (i, v))
  g.writeln('}')
  return file_path

def gen_config_h(os):
  file_path = bb.host_os.path.join(bb.env.pwd(), 'config_autogen.h')
  g = CGenerator().create(file_path)
  g.writeln('#define BBOS_MAX_MESSAGE_SIZE 10')
  g.writeln('#define BBOS_NR_THREADS %d' % os.get_num_threads())
  g.writeln("/* Thread id's and runners */")
  for i, thread in enumerate(os.get_threads()):
    g.writeln("#define %s %d" % (thread.get_name(), i))
    g.writeln("#define %s_RUNNER %s" % \
                (thread.get_name(), thread.get_runner()))
  g.writeln('/* Supported messages */')
  for i, message in enumerate(os.get_messages()):
    g.writeln('#define %s %d' % (message.id, i))
  g.close()

with OS as bundle:
  bundle.build_cases.update({
    # Propeller GCC compiler support
    'propeller' : {
      'sources': ('../os.c', 'mm/mempool.c', gen_os_c, gen_config_h,)
    }
  })
