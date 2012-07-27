#!/usr/bin/env python

from bb import builder

builder.rule('bb.os.os.OS', {
    'PropellerToolchain' : {
      'srcs': ('kernel.c')
      }
})
