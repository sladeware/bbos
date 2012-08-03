#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import bb
from bb.cli import CLI

if __name__ == '__main__':
  CLI.config.parse_command_line()
  command = CLI.config.command
  command()
