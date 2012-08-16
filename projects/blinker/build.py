#!/usr/bin/env python

import bb
from bb import Builder

Builder.rule(bb.application.get_mapping('Blinker').get_thread('B0'), {
    'PropellerToolchain' : {
      'srcs' : ('b0.c',)
      }
    })
Builder.rule(bb.application.get_mapping('Blinker').get_thread('B1'), {
    'PropellerToolchain' : {
      'srcs' : ('b1.c',)
      }
    })
Builder.build()
