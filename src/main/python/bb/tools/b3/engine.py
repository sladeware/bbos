# -*- coding: utf-8; -*-
#
# http://www.bionicbunny.org/
# Copyright (c) 2013 Sladeware LLC
#
# Author: Oleksandr Sviridenko <info@bionicbunny.org>

from __future__ import print_function

import logging
import pkgutil
import inspect
import os
import sys
import optparse
import traceback

from bb.utils import typecheck
from bb.tools.b3 import commands
from bb.tools.b3 import rules
from bb.tools.b3 import buildfile
from bb.tools.b3.commands.command import Command

__version__ = "0.0.1"

_buildroot = None
_commands = {}

DEFAULT_COMMAND = "build"

def get_version():
  return __version__

def get_build_root():
  return os.getcwd()

def exit_and_fail(msg, exit_code=1):
  """Prints msg to STDERR and exits with exit_code."""
  if msg:
    print(msg, file=sys.stderr)
  sys.exit(exit_code)

def trace_exception_and_exit():
  print()
  print("_" * 70)
  print()
  print("EXCEPTION")
  print("_" * 70)
  print()
  traceback.print_exc(file=sys.stdout)
  print("_" * 70)
  sys.exit(0)

def synthesize_command(root_dir, args):
  command = args[0] if len(args) else DEFAULT_COMMAND
  if command in get_all_commands():
    subcommand_args = args[1:] if len(args) > 1 else []
    return command, subcommand_args
  else:
    exit_and_fail("Invalid command: %s" % command)
  return command, None

def get_command(name):
  return _commands.get(name, None)

def get_all_commands():
  return _commands.keys()

def register_commands():
  """Registers commands from bb.tools.b3.commands package."""
  for _, mod, ispkg in pkgutil.iter_modules(commands.__path__):
    if ispkg: continue
    fq_module = '.'.join([commands.__name__, mod])
    __import__(fq_module)
    for (_, cls) in inspect.getmembers(sys.modules[fq_module], inspect.isclass):
      if issubclass(cls, Command) and not cls is Command:
        _commands[cls.__name__.lower()] = cls

def parse_command(root_dir, args):
  command, args = synthesize_command(root_dir, args)
  return get_command(command), args

def register_rules():
  """Registers rules from bb.tools.b3.rules package."""
  for _, mod, ispkg in pkgutil.iter_modules(rules.__path__):
    if ispkg:
      continue
    fq_module = '.'.join([rules.__name__, mod])
    __import__(fq_module)
    for (_, cls) in inspect.getmembers(sys.modules[fq_module], inspect.isclass):
      if issubclass(cls, buildfile.Rule):
        setattr(sys.modules[__name__], cls.__name__, cls)

def run():
  version = get_version()
  rootdir = get_build_root()
  print("b3 v%s" % version)
  command_class, command_args = parse_command(rootdir, sys.argv[1:])
  parser = optparse.OptionParser(version='b3 %s' % version)
  command = command_class(rootdir, parser, command_args)
  if command.serialized():
    raise NotImplementedError()
  else:
    lock = None #Lock.unlocked()
  try:
    result = command.run(lock)
    sys.exit(result)
  except KeyboardInterrupt:
    command.cleanup()
    raise
  finally:
    # lock.release()
    pass

def main():
  register_rules()
  register_commands()
  try:
    run()
  except KeyboardInterrupt:
    exit_and_fail("Interrupted by user.")
  except SystemExit, e:
    if e.code > 0:
      trace_exception_and_exit()
  except:
    trace_exception_and_exit()
  return 0
