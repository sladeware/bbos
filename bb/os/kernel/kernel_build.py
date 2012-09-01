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

with Kernel as bundle:
  def dependency_resolver(x, kernel):
    return kernel.get_threads() + [kernel.get_scheduler()]
  bundle.decomposer = dependency_resolver

def gen_main_c(kernel):
  if not kernel.get_core():
    raise Exception("Core wasn't assigned to the this kernel!")
  file_path = os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'main%d_autogen.c' %
                           kernel.get_core().get_id())
  g = CGenerator().create(file_path)
  g.writeln('#include <bb/os.h>')
  g.writeln()
  g.writeln('/* PROTOTYPES */');
  g.writeln('static void bbos_loop();');
  g.writeln()
  # Generate necessary API for static scheduler
  if isinstance(kernel.get_scheduler(), StaticScheduler):
    g.writeln('static void')
    g.writeln('bbos_loop()')
    g.writeln('{')
    g.writeln('  while (1) {')
    for thread in kernel.get_threads():
      g.writeln('    %s();' % thread.get_runner())
    g.writeln('  }')
    g.writeln('}')
  # Init
  g.writeln('static void')
  g.writeln('bbos_init()')
  g.writeln('{')
  #g.write('  BBOS_SET_NR_THREADS(%d);\n' % os.kernel.get_num_threads())
  #g.write('  BBOS_KERNEL_SET_RUNNING_TYPE(%d);\n' % 0)
  g.writeln('}')
  g.writeln()
  g.writeln('static void')
  g.writeln('bbos_start()')
  g.writeln('{')
  #g.write('  bbos_kernel_start();\n')
  g.writeln('  bbos_loop();')
  g.writeln('}')
  g.writeln()
  g.writeln('void')
  g.writeln('main%d(void* arg)' % kernel.get_core().get_id())
  g.writeln('{')
  g.writeln('  bbos_init();')
  g.writeln('  bbos_start();')
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
