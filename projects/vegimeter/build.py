#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from vegimeter import vegimeter

import bb
from bb.application_build import Application

vegimeter = bb.application.get_mapping('Vegimeter')
if not vegimeter:
  print "Application doesn't have mapping Vegimeter."
  print "Nothing to build. Exit."
  exit(0)

bb.Builder.rule(vegimeter.get_thread('UI'), {
    'PropellerToolchain' : {
      'srcs' : ('ui.c',)
      }
    })
bb.Builder.rule(vegimeter.get_thread('BUTTON_DRIVER'), {
    'PropellerToolchain' : {
      'srcs' : ('button_driver.c',)
      }
    })

bb.Builder.set_application_class(Application)
