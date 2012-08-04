#!/usr/bin/env python

import bb
from bb.tools import propler

bb.builder.rule(bb.application.get_mapping('Blinker').get_thread('BLINKER'), {
    'PropellerToolchain' : {
      'srcs' : ('blinker.c',)
      }
    })

bb.builder.build()

#uploader = propler.SPIUploader()
