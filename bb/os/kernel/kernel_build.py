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

import os.path

import bb
from bb.os import Kernel
from bb.os.kernel.schedulers import StaticScheduler
from bb.tools.generators import CGenerator

def gen_main_c(kernel):
  if not kernel.get_core():
    raise Exception("Core wasn't assigned to the this kernel!")
  file_path = os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'main%d_autogen.c' %
                           kernel.get_core().get_id())
  g = CGenerator().create(file_path)
  g.writeln('#define BBOS_KERNEL_ID %d' % kernel.get_core().get_id())
  g.writeln('')
  g.writeln('#include <bb/os.h>')
  g.writeln('#include BBOS_PROCESSOR_FILE(init.h)')
  g.writeln()
  # Generate necessary API for static scheduler
  if isinstance(kernel.get_scheduler(), StaticScheduler):
    g.writeln('static void')
    g.writeln('loop()')
    g.writeln('{')
    g.writeln('  while (1) {')
    for thread in kernel.get_threads():
      g.writeln('    bbos_set_running_thread(%s);' % thread.get_name())
      g.writeln('    %s();' % thread.get_runner())
    g.writeln('  }')
    g.writeln('}')
  # Init
  g.writeln('static void')
  g.writeln('init()')
  g.writeln('{')
  #g.writeln('  bbos_kernel_init();')
  #g.write('  BBOS_SET_NR_THREADS(%d);\n' % os.kernel.get_num_threads())
  #g.write('  BBOS_KERNEL_SET_RUNNING_TYPE(%d);\n' % 0)
  g.writeln('}')
  g.writeln()
  g.writeln('static void')
  g.writeln('start()')
  g.writeln('{')
  #g.writeln('  bbos_kernel_start();\n')
  g.writeln('  loop();')
  g.writeln('}')
  g.writeln()
  g.writeln('void')
  g.writeln('main%d(void* arg)' % kernel.get_core().get_id())
  g.writeln('{')
  g.writeln('  init();')
  g.writeln('  start();')
  g.writeln('}')
  return file_path

def update_bbos_config_h(kernel):
  file_path = os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'config_autogen.h')
  g = CGenerator().edit(file_path)
  for thread in kernel.get_threads():
    g.writeln('void %s();' % thread.get_runner())
  g.close()

with Kernel as bundle:
  bundle.build_cases.update({
    'propeller': {
      'sources': (gen_main_c, update_bbos_config_h,
                  './../kernel.c')
      }
    })
