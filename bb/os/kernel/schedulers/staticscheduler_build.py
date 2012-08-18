#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import bb
from bb import Builder
from bb.os.kernel.schedulers import StaticScheduler

def update_main_c(scheduler):
  kernel = Builder.context['kernel']
  if not kernel:
    raise Exception('Fix this')
  file_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb", "os", "main%d_autogen.c" % kernel.get_core().get_id())
  fh = open(file_path, 'a')
  fh.write('\n')
  fh.write("static void bbos_loop() {\n")
  fh.write('  while (1) {\n')
  for thread in kernel.get_threads():
    fh.write('    %s();\n' % thread.get_runner())
  fh.write('  }\n')
  fh.write('}\n')
  fh.close()

Builder.rule(StaticScheduler, {
    'PropellerToolchain' : {
      'srcs': (update_main_c,),
    }})
