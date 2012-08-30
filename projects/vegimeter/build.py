#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from vegimeter import vegimeter

import bb

vegimeter = bb.application.get_mapping('Vegimeter')

with vegimeter.get_thread('UI') as target:
  target.build_cases += {
    'propeller' : {
      'sources' : ('ui.c',)
      }
    }

with vegimeter.get_thread('CONTROL_PANEL') as target:
  target.build_cases += {
    'propeller' : {
      'sources' : ('control_panel.c',)
      }
    }
