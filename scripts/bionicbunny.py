#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import bb
from bb.cli import CLI

if __name__ == '__main__':
  CLI.config.parse_command_line()
  command = CLI.config.command
  try:
    command()
  except Exception, e:
    print e
    exit(1)
