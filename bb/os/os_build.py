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

# TODO(team): the following code has to be moved with all C files, once C
# implementation will be separated.

_CFG = {
  'BBOS_MESSAGE_SIZE': 0,
  'BBOS_NUM_THREADS': 0,
  'BBOS_NUM_PORTS': 0,
  'BBOS_NUM_KERNELS': 0,
}

def gen_os_c(os):
  sorted_threads = filter(lambda thread: thread.has_port(),
                          sorted(os.get_threads(),
                                 key=lambda thread: thread.has_port(),
                                 reverse=True))
  file_path = bb.host_os.path.join(bb.env.pwd(), '..', 'os_autogen.c')
  g = CGenerator().create(file_path)
  g.writeln('#include "os.h"')
  g.writeln()
  for i, thread in enumerate(sorted_threads):
    g.writeln('MEMPOOL_PARTITION(port%d_part, %d, BBOS_MESSAGE_SIZE);' % (i, thread.get_port().get_capacity()))
    g.writeln('bbos_message_t* port%d_stack[%d];' % (i, thread.get_port().get_capacity()))
  g.writeln()
  g.writeln('bbos_port_t bbos_ports[BBOS_NUM_PORTS];')
  g.writeln()
  g.writeln('void')
  g.writeln('bbos_init()')
  g.writeln('{')
  for i, thread in enumerate(sorted_threads):
    port = thread.get_port()
    g.writeln('  mempool_t port%d_pool = mempool_init(port%d_part, %d, %s);' % \
                  (i, i, port.get_capacity(), 'BBOS_MESSAGE_SIZE'))
    g.writeln('  bbos_port_init(%d, %d, port%d_pool, port%d_stack);' % (i, port.get_capacity(), i, i))
  g.writeln('}')
  return file_path

def gen_config_h(os):
  """Generate bb/os/config_autogen.h header file. Will be included by
  bb/os/config.h header file.
  """
  _CFG.update(
    BBOS_NUM_THREADS=os.get_num_threads(),
    BBOS_NUM_PORTS=sum([thread.has_port() for thread in os.get_threads()]),
    BBOS_MESSAGE_SIZE=2,
    BBOS_NUM_KERNELS=os.get_num_kernels()
    )
  file_path = bb.host_os.path.join(bb.env.pwd(), 'config_autogen.h')
  g = CGenerator().create(file_path)
  for key, value in _CFG.items():
    g.writeln('#define %s %d' % (key, value))
  g.writeln("/* Thread id's and runners */")
  sorted_threads = sorted(os.get_threads(), key=lambda thread: thread.has_port(), reverse=True)
  for i, thread in enumerate(sorted_threads):
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
      'sources': ('../os.c', 'port.c', 'mm/mempool.c', gen_os_c, gen_config_h,)
    }
  })
