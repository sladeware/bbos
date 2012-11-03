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
from bb.os.drivers.processors import PropellerP8X32ADriver
from bb.tools.generators import CGenerator
from bb.tools.compilers import PropGCC

def update_bbos_config_h(processor):
  file_path = bb.host_os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'config_autogen.h')
  g = CGenerator().edit(file_path)
  g.writeln("#define BBOS_CONFIG_PROCESSOR propeller_p8x32")
  g.close()

def gen_main_c(processor):
  os = processor.get_os()
  file_path = bb.host_os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'main_autogen.c')
  g = CGenerator().create(file_path)
  # Do all necessary includes
  g.writeln('#include <bb/os.h>')
  g.writeln('#include "main.h"')
  g.writeln('#include <propeller.h>')
  g.writeln('#include <sys/thread.h>')
  g.writeln()
  # Initialize thread data
  # TODO(team): the stack size has to be consider for each thread individually.
  stack_size = 16
  for kernel in os.get_kernels():
    g.writeln('static _thread_state_t thread%d_data;' %
              kernel.get_core().get_id())
    g.writeln('static int cog%d_stack[%d];' % (kernel.get_core().get_id(),
                                               stack_size))
  g.writeln()
  # Write the main entry point
  g.writeln('int')
  g.writeln('main()')
  g.writeln('{')
  g.writeln('  bbos(); /* BBOS entry point */')
  for kernel in os.get_kernels():
    core = kernel.get_core()
    g.writeln('  _start_cog_thread(cog%d_stack + 16, main%d, (void*)0, '\
                '&thread%d_data);' % (core.get_id(), core.get_id(),
                                      core.get_id()))
  g.writeln('  return 0;')
  g.writeln('}')
  g.close()
  return file_path

def gen_main_h(processor):
  os = processor.get_os()
  file_path = bb.host_os.path.join(bb.env['BB_HOME'], 'bb', 'os', 'main_autogen.h')
  g = CGenerator().create(file_path)
  for kernel in os.get_kernels():
    core = kernel.get_core()
    g.writeln('void main%d(void* arg);' % core.get_id());
  g.close()

PropellerP8X32ADriver.Builder += PropGCC.Parameters(
  sources=(gen_main_c, gen_main_h, update_bbos_config_h,
           'propeller_p8x32/cog.c', 'propeller_p8x32/delay.c',
           'propeller_p8x32/sio.c')
  )
