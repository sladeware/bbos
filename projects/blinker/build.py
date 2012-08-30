#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import bb

import blinker

blinker = bb.application.get_mapping('Blinker')

with blinker.get_thread('B0') as target:
  target.build_cases += {
    'propeller': {
      'sources': ('b0.c',)
      }
    }

with blinker.get_thread('B1') as target:
  target.build_cases += {
    'propeller': {
      'sources': ('b1.c',)
      }
    }
