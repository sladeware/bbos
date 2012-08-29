#!/usr/bin/env python

import logging
import imp

import bb
from bb.tools import builder
from bb.tools.loaders import propler

    #for image in bb.Builder.get_application().get_images():
    #  uploader = propler.SPIUploader(port='/dev/ttyUSB0')
    #  if not uploader.connect():
    #    sys.exit(1)
    #  uploader.upload_file(image.get_name(), eeprom=False)
    #  uploader.disconnect()

def _import_load_scripts():
  load_script_filename = "load.py"
  load_script_path = bb.host_os.path.join(bb.env['BB_APPLICATION_HOME'],
                                          load_script_filename)
  if not bb.host_os.path.exists(load_script_path):
    logging.warning("Load-script '%s' doesn't exist" % load_script_path)
  else:
    logging.debug("Import script: %s" % load_script_path)
    imp.load_source('bb.load', load_script_path)

def upload():
  bb.next_stage()
  _import_load_scripts()
