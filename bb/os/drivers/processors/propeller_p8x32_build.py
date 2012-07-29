#!/usr/bin/env python

import bb
from bb.config import host_os
from bb import builder

def update_bbos_config_h(processor):
  file_path = host_os.path.join(bb.env["BB_HOME"], "bb", "os", "config_autogen.h")
  fh = open(file_path, 'a')
  fh.write("#define BBOS_CONFIG_PROCESSOR propeller_p8x32\n")
  fh.close()

builder.rule('bb.hardware.devices.processors.propeller_p8x32.PropellerP8X32A', {
    'PropellerToolchain' : {
      'srcs': (update_bbos_config_h,
               "propeller_p8x32/cog.c", "propeller_p8x32/delay.c")
      }
})
