#!/usr/bin/env python

from bb import builder
import model

builder.rule(model.printer, {
    'PropellerToolchain': {
      'srcs': ('helloworld.c',)
      }
    })
