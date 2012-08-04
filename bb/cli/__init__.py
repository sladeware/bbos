#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.cli.command_line_interface import CommandLineInterface, CLI
import bb.cli.config
from bb.cli import commands

for command_name in commands.__all__:
  command_class = getattr(commands, command_name, None)
  if not command_class:
    raise Exception('command cannot be found')
  command = command_class()
  CLI.register_command(command_name, command)
