#!/usr/bin/env python

import bb
from bb.tools import propler

bb.builder.rule(bb.application.get_mapping('Blinker').get_thread('BLINKER'), {
    'PropellerToolchain' : {
      'srcs' : ('blinker.c',)
      }
    })
bb.builder.build()

#uploader = propler.SPIUploader(port='/dev/ttyUSB0')
#if not uploader.connect():
#  exit(1)
#uploader.upload_file('Blinker_0', eeprom=True)
#uploader.disconnect()
