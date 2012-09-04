#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import sys

import bb
from bb.tools.loaders import propler

import vegimeter

vegimeter = bb.application.get_mapping('Vegimeter')
processor =  vegimeter.get_processor()
with processor.get_os() as binary:
  # TODO(team): this is straight-forward implementation.
  #             Should be replaced soon.
  uploader = propler.SPIUploader(port='/dev/ttyUSB0')
  if not uploader.connect():
    sys.exit(1)
  uploader.upload_file(binary.get_filename(), eeprom=False)
  propler.terminal_mode()
  uploader.disconnect()
