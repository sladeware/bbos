#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.os.drivers.processors.propeller_p8x32 import shmem

with shmem.ShMemDriver as target:
  target.build_cases.update({
      'propeller': {
        'sources': ('shmem.c',)
        }
      })
