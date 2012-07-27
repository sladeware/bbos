#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import logging

import bb
from bb.cli import CLI

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
  CLI.config.parse_command_line()
  action = CLI.config.action
  try:
    action()
  except Exception, e:
    print e
    exit(1)
