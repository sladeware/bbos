#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from bb import builder

import bb
from bb import Builder
from bb.os.kernel.schedulers import StaticScheduler

def update_bbos_config_h(kernel):
  file_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb", "os", "config_autogen.h")
  fh = open(file_path, 'a')
  for thread in kernel.get_threads():
    fh.write("void %s();\n" % thread.get_runner())
  fh.close()

Builder.rule('bb.os.kernel.kernel.Kernel', {
    'PropellerToolchain': {
      'srcs': (update_bbos_config_h,)
      }
    })
