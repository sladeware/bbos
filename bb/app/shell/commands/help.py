#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware"
__author__ = "Oleksandr Sviridenko"

import sys

from bb.shell.commands.command import Command

class help(Command):
  USAGE = '%prog help <command>'
  SHORT_DESC = 'Print help for a specific command'
  USES_BASEPATH = False

  def function(self, command_name=None):
    """Prints help for a specific command.

    Args:
    command: If provided, print help for the action provided.

    Expects self.args[0], or 'command', to contain the name of the action in
    question. Exits the program after printing the help message.
    """
    if not command_name:
      if len(CLI.config.args) >= 1:
        CLI.config.args = [' '.join(CLI.config.args)]
      if len(CLI.config.args) != 1 or \
            not CLI.is_supported_command(CLI.config.args[0]):
        CLI.config.optparser.error('Expected a single command argument. '
                                   ' Must be one of:\n' +
                                   CLI.get_command_descriptions())
      command_name = CLI.config.args[0]
    command = CLI.get_command(command_name)
    optparser, unused_options = CLI.config._make_specific_parser(command)
    optparser.print_help()
    sys.exit(0)
