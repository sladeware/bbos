#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from vegimeter import vegimeter

import bb

vegimeter = bb.application.get_mapping('Vegimeter')
if not vegimeter:
  print "Application doesn't have mapping Vegimeter."
  print "Nothing to build. Exit."
  exit(0)

if vegimeter.get_thread('UI'):
  with vegimeter.get_thread('UI') as target:
    target.build_cases += {
      'propeller' : {
        'sources' : ('ui.c',)
        }
      }

if vegimeter.get_thread('BUTTON_DRIVER'):
  with vegimeter.get_thread('BUTTON_DRIVER') as target:
    target.build_cases += {
      'propeller' : {
        'sources' : ('button_driver.c',)
        }
      }
