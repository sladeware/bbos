#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import bb
from bb.application_build import Application

bb.Builder.rule(bb.application.get_mapping('Blinker').get_thread('B0'), {
    'PropellerToolchain' : {
      'srcs' : ('b0.c',)
      }
    })
bb.Builder.rule(bb.application.get_mapping('Blinker').get_thread('B1'), {
    'PropellerToolchain' : {
      'srcs' : ('b1.c',)
      }
    })

bb.Builder.set_application_class(Application)
