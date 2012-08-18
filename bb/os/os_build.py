#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import collections

import bb
from bb.lib.build.generators import CGenerator

autogen_dir_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb")

def gen_config_h(os):
  bb.Builder.context['OS'] = os
  file_path = bb.host_os.path.join(autogen_dir_path, 'os', 'config_autogen.h')
  g = CGenerator().create(file_path)
  #fh.write("#define BBOS_CONFIG_NR_THREADS %d\n" % os.kernel.get_num_threads())
  for kernel in os.get_kernels():
    for i in range(kernel.get_num_threads()):
      thread = kernel.get_threads()[i]
      g.writeln("#define %s %d" % (thread.get_name(), i))
      g.writeln("#define %s_RUNNER %s" % (thread.get_name(), thread.get_runner()))
  g.close()

bb.Builder.rule('bb.os.os.OS', {
    'PropellerToolchain' : {
      'srcs': ('kernel.c', gen_config_h)
      }
})
