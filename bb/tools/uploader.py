#!/usr/bin/env python

import logging
import imp

import bb
from bb.tools import builder
from bb.tools.loaders import propler

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
