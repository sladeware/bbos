#!/usr/bin/env python

import bb

print (bb.application.get_mapping('Blinker').get_thread('B0'),)
print (bb.application.get_mapping('Blinker').get_thread('B1'),)

bb.builder.rule(bb.application.get_mapping('Blinker').get_thread('B0'), {
    'PropellerToolchain' : {
      'srcs' : ('b0.c',)
      }
    })
bb.builder.rule(bb.application.get_mapping('Blinker').get_thread('B1'), {
    'PropellerToolchain' : {
      'srcs' : ('b1.c',)
      }
    })
bb.builder.build()
