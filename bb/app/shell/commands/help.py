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

import sys

import bb
from bb.app.shell.commands.command import Command

class help(Command):

  USAGE = '%prog help <command>'
  SHORT_DESC = "Print help for a specific command"
  USES_BASEPATH = False

  def run(self, name=None):
    """Prints help for a specific command.

    If `command` provided, print help for the action provided.

    Expects `self.args[0]`, or 'command', to contain the name of the action in
    question. Exits the program after printing the help message.
    """
    app = bb.get_app()
    shell = app.get_shell()
    if not name:
      print "Expected a single command argument. Must be one of:"
      print shell.get_command_descriptions()
      sys.exit(0)
    if not shell.is_supported_command(name):
      print "Command '%s' is not supported. Must be one of:" % name
      print shell.get_command_descriptions()
      sys.exit(0)
    command = shell.get_command(name)
    optparser, unused_options = shell._make_specific_parser(command)
    optparser.print_help()
    sys.exit(0)
