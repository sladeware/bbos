#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import imp
import os
import sys
import traceback

import bb
from bb.cli.commands.command import Command
#from bb.tools import propler

class load(Command):
  USAGE = '%prog load'
  SHORT_DESC = 'Load a binary'
  USES_BASEPATH = False

  def function(self):
    build_script_filename = "build.py"
    build_script_path = os.path.join(bb.env['BB_APPLICATION_HOME'],
                                     build_script_filename)
    if not os.path.exists(build_script_path):
      print "Build script '%s' doesn't exist" % build_script_path
      sys.exit(0)
    print "Run build script: %s" % build_script_path

    if os.path.exists(build_script_path):
      imp.load_source('bb.buildtime.application.build', build_script_path)
    bb.Builder.prepare()
    #for image in bb.Builder.get_application().get_images():
    #  uploader = propler.SPIUploader(port='/dev/ttyUSB0')
    #  if not uploader.connect():
    #    sys.exit(1)
    #  uploader.upload_file(image.get_name(), eeprom=False)
    #  uploader.disconnect()
