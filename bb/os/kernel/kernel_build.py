#!/usr/bin/env python

from bb import builder

import bb
from bb.config import host_os
from bb import builder
from bb.os.kernel.schedulers import StaticScheduler

def update_bbos_config_h(kernel):
  file_path = host_os.path.join(bb.env["BB_HOME"], "bb", "os", "config_autogen.h")
  fh = open(file_path, 'a')
  for thread in kernel.get_threads():
    fh.write("void %s();\n" % thread.get_runner())
  if isinstance(kernel.get_scheduler(), StaticScheduler):
    fh.write("#define BBOS_CONFIG_KERNEL_LOOP() do {\\\n")
    fh.write("  while (1) {\\\n")
    for thread in kernel.get_threads():
      fh.write("    %s();\\\n" % thread.get_runner())
    fh.write("  }\\\n")
    fh.write("} while (0)\n")
  fh.close()

builder.rule('bb.os.kernel.kernel.Kernel', {
    'PropellerToolchain': {
      'srcs': (update_bbos_config_h,)
      }
    })
