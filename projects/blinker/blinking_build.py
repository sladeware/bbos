#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb

import blinking

# Thread B0
with blinking.blinker.get_thread('B0') as bundle:
  bundle.build_cases += {
    'propeller': {
      'sources': ('b0.c',)
      }
    }

# Thread B1
with blinking.blinker.get_thread('B1') as bundle:
  bundle.build_cases += {
    'propeller': {
      'sources': ('b1.c',)
      }
    }
