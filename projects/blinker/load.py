#!/usr/bin/env python

__author__ = 'Oleksandr Sviridenko'

import sys

import bb
from bb.tools.loaders import propler

import blinking

(processor,) =  blinking.blinker.get_board().get_processors()
with processor.get_os() as binary:
  # Straight-forward implementation. Will be replaced soon.
  uploader = propler.SPIUploader(port='/dev/ttyUSB0')
  if not uploader.connect():
    sys.exit(1)
  uploader.upload_file(binary.get_filename(), eeprom=False)
  uploader.disconnect()
