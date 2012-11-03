#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.tools.compilers import PropGCC

import shmem

shmem.ShMemDriver.Builder += PropGCC.Parameters(
  sources=('shmem.c',)
)
