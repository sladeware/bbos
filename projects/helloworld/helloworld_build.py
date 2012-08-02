#!/usr/bin/env python

import bb

hello_world = bb.application.get_mapping("HELLO_WORLD")
bb.builder.rule(hello_world.get_thread("PRINTER"), {
    'PropellerToolchain': {
      'srcs': ('helloworld.c',)
      }
    })
