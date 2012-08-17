#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import imp
import os
import sys
import traceback

import bb
import bb.config.importing as bbimport
from bb.cli.command_line_interface import CLI
from bb.cli.commands.command import Command

class build(Command):
  USAGE = '%prog build'
  SHORT_DESC = 'Build an application'
  USES_BASEPATH = False

  def function(self):
    build_script_filename = "build.py"
    build_script_path = os.path.join(bb.env["BB_APPLICATION_HOME"],
                                     build_script_filename)
    if not os.path.exists(build_script_path):
      print "Build script '%s' doesn't exist" % build_script_path
      sys.exit(0)
    print "Run build script: %s" % build_script_path
    try:
      bbimport.import_build_scripts()
      if os.path.exists(build_script_path):
        imp.load_source('bb.buildtime.application.build', build_script_path)
    except SystemExit, e:
      if e.code > 0:
        self._build_exception()
    except:
      self._build_exception()

  def _build_exception(self):
    print '=' * 70
    print 'Exception in build script'
    print '=' * 70
    traceback.print_exc(file=sys.stdout)
    print '_' * 70

  def options(self, config, optparser):
    optparser.add_option('--list-toolchains',
                         dest='list_toolchains',
                         action='store_true',
                         help='List supported toolchains.')
    optparser.add_option('--verbose',
                         dest='verbose',
                         type='int',
                         default=0,
                         help='Verbose level.')
    optparser.add_option('--dry-run',
                         action='store_true',
                         dest='dry_run',
                         help='Show only messages that would be printed in a real run.')
