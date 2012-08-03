#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import imp
<<<<<<< HEAD
import os
=======
>>>>>>> upstream/master
import sys
import traceback

import bb
from bb.cli import CLI
from bb.config import host_os
import bb.config.importing as bbimport

@CLI.command(usage='%prog help <command>',
             short_desc='Print help for a specific command',
             uses_basepath=False)
def help(command_name=None):
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

def _perform_build_options(config, optparser):
  optparser.add_option('--list-toolchains',
                       dest='list_toolchains',
                       action='store_true',
                       help='List supported toolchains.')
  optparser.add_option('--dry-run',
                       dest='dry_run',
                       action='store_true',
                       help='Dry run mode.')
  optparser.add_option('--dry-run',
                       action='store_true',
                       dest='dry_run',
                       help='Show only messages that would be printed in a real run.')

@CLI.command(usage='%prog build',
             options=_perform_build_options,
             short_desc='Build an application',
             uses_basepath=False)
def build():
  model_filename = None
  model_path = None
  if len(CLI.config.args) > 0:
    model_filename= CLI.config.args[0]
    model_path = host_os.path.join(bb.env["BB_APPLICATION_HOME"], model_filename)
  if not model_path:
    raise Exception("model_path")
<<<<<<< HEAD
  if not os.path.exists(model_path):
    raise Exception("mode %s doesn't exist" % model_path)
=======
>>>>>>> upstream/master
  build_script_filename = "build.py"
  build_script_path = host_os.path.join(bb.env["BB_APPLICATION_HOME"],
                                        build_script_filename)
  if not host_os.path.exists(build_script_path):
    print "Build script '%s' doesn't exist" % build_script_path
  print "Run build script: %s" % build_script_path
  try:
    imp.load_source('model', model_path) # TODO: right module name
    bbimport.import_build_scripts()
<<<<<<< HEAD
    if os.path.exists(build_script_path):
      imp.load_source('bb.buildtime.application.build', build_script_path)
=======
    imp.load_source('bb.buildtime.application.build', build_script_path)
>>>>>>> upstream/master
  except SystemExit, e:
    if e.code > 0:
      _build_exception()
  except:
    _build_exception()

def _build_exception():
    print '=' * 70
    print "Exception in build script"
    print '=' * 70
    traceback.print_exc(file=sys.stdout)
    print '_' * 70
