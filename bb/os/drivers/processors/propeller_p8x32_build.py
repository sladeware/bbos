#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

import os

import bb

def update_bbos_config_h(processor):
  file_path = os.path.join(bb.env["BB_HOME"], "bb", "os", "config_autogen.h")
  fh = open(file_path, 'a')
  fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")
  fh.close()

bb.builder.rule('bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A', {
    'PropellerToolchain' : {
      'srcs': (update_bbos_config_h,
               "propeller_p8x32/cog.c", "propeller_p8x32/delay.c")
      }
})
