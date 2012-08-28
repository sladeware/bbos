#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import imp
import os
import sys
import traceback
import logging

import bb
from bb.cli.commands.command import Command
from bb.tools import builder
from bb.tools import uploader
#from bb.tools import propler

class load(Command):
  USAGE = '%prog load'
  SHORT_DESC = 'Load a binary'
  USES_BASEPATH = False

  def function(self):
    load_script_filename = "load.py"
    load_script_path = os.path.join(bb.env['BB_APPLICATION_HOME'],
                                    load_script_filename)
    if not os.path.exists(load_script_path):
      logging.warning("Load script '%s' doesn't exist" % load_script_path)
    else:
      print "Run load script: %s" % load_script_path
      imp.load_source('bb.loadtime.load', load_script_path)
    builder.build()
    #bb.Builder.prepare()
    #for image in bb.Builder.get_application().get_images():
    #  uploader = propler.SPIUploader(port='/dev/ttyUSB0')
    #  if not uploader.connect():
    #    sys.exit(1)
    #  uploader.upload_file(image.get_name(), eeprom=False)
    #  uploader.disconnect()
