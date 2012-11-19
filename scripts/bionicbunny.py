#!/usr/bin/env python

import sys
import traceback

import bb

def trace_exception_and_exit():
  print
  print "_" * 70
  print
  print "EXCEPTION"
  print "_" * 70
  print
  traceback.print_exc(file=sys.stdout)
  print "_" * 70
  sys.exit(0)

def main():
  app = bb.get_app()
  if not app:
    raise Exception()
  shell = app.get_shell()
  try:
    shell.run()
  except SystemExit, e:
    if e.code > 0:
      trace_exception_and_exit()
  except:
    trace_exception_and_exit()
  return 0

if __name__ == "__main__":
  sys.exit(main())
