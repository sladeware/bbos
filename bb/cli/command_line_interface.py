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

class _CommandLineInterface(object):
  config = None
  commands = dict()

  def __init__(self):
    pass

  def get_commands(self):
    return self.commands.values()

  def get_command_names(self):
    return self.commands.keys()

  def register_command(self, name, command):
    self.commands[name] = command

  def is_supported_command(self, name):
    return name in self.get_command_names()

  def get_command(self, name):
    return self.commands[name]

  def get_command_descriptions(self):
    """Returns a formatted string containing the short_descs for all
    commands.
    """
    cmd_names = self.commands.keys()
    cmd_names.sort()
    desc = ''
    max_cmd_name_len = 0
    for cmd_name in cmd_names:
      if len(cmd_name) > max_cmd_name_len:
        max_cmd_name_len = len(cmd_name)
    cmd_desc_frmt = '  %{0}s  %s\n'.format(max_cmd_name_len)
    for cmd_name in cmd_names:
      if not self.commands[cmd_name].hidden:
        desc += cmd_desc_frmt % (cmd_name,
                                self.commands[cmd_name].short_desc)
    return desc

  def command(self, usage, short_desc, uses_basepath=False,
              options=lambda obj, parser: None):
    def _(function):
      cmd = Command(function, usage, short_desc, uses_basepath,
                    options=options)
      self.register_command(function.__name__, cmd)
      return function
    return _

CLI = CommandLineInterface = _CommandLineInterface()
