#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import sys
import traceback

import bb
from bb.cli import CLI

def trace_exception_and_exit():
  print
  print '=' * 70
  print 'EXCEPTION'
  print '=' * 70
  traceback.print_exc(file=sys.stdout)
  print '_' * 70
  sys.exit(0)

if __name__ == '__main__':
  CLI.config.parse_command_line()
  command = CLI.config.command
  try:
    command()
  except SystemExit, e:
    if e.code > 0:
      trace_exception_and_exit()
  except:
    trace_exception_and_exit()
