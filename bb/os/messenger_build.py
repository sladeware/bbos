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
__author__ = "Oleksandr Sviridenko"

import inspect

import bb
from bb.os.messenger import Messenger
from bb.tools.generators import CGenerator
from bb.tools.compilers import PropGCC

def gen_runner_h(messenger):
  """Generates runner's header file. The file will be stored in the
  same directory, where the build file is located or in the current
  directory.
  """
  dir_path = '.'
  if messenger.__class__ is not Messenger:
    dir_path = bb.host_os.path.dirname(inspect.getmodule(messenger).__file__)
  file_path = bb.host_os.path.join(dir_path, messenger.get_runner() + '_autogen.h')
  g = CGenerator().create(file_path)
  g.writeln('#include <bb/os.h>')
  g.writeln()
  g.writeln('void %s();' % messenger.get_runner())

def gen_runner_c(messenger):
  dir_path = '.'
  if messenger.__class__ is not Messenger:
    dir_path = bb.host_os.path.dirname(inspect.getmodule(messenger).__file__)
  file_path = bb.host_os.path.join(dir_path, messenger.get_runner() + '_autogen.c')
  g = CGenerator().create(file_path)
  g.writeln('void %s()' % messenger.get_runner())
  g.writeln('{')
  g.writeln('  bbos_message_t* request;')
  g.writeln('  bbos_message_t* response;')
  g.writeln('  if ((request = bbos_receive_message()) == NULL) {')
  if messenger.get_default_action():
    g.writeln('    %s();' % messenger.get_default_action())
  g.writeln('    return;')
  g.writeln('  }')
  g.writeln('  switch (request->label) {')
  for message in messenger.get_supported_messages():
    handler = messenger.get_message_handler(message)
    g.writeln('   case %s:' % message.label)
    if message.output_fields:
      g.writeln('     if ((response = bbos_send_message(request->sender)) == NULL) {')
      g.writeln('       break;')
      g.writeln('     }')
      g.writeln('     %s(&request->payload, &response->payload);' % handler)
    else:
      g.writeln('     %s(&request->payload);' % handler)
    g.writeln('     break;')
  g.writeln('  }')
  g.writeln('  bbos_deliver_messages();')
  g.writeln('}')
  g.close()

Messenger.Builder += PropGCC.Parameters(
  sources=(gen_runner_c, gen_runner_h),
  )
