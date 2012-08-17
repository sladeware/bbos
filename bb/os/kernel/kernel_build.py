#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

from bb import builder

import bb
from bb.os.kernel.schedulers import StaticScheduler

def gen_main_c(kernel):
  bb.Builder.context['kernel'] = kernel
  file_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb", "os", "main%d_autogen.c" % kernel.get_core().get_id())
  fh = open(file_path, 'w')
  #fh.write(autogen_header)
  fh.write("#include <bb/os.h>\n\n")

  fh.write('/* PROTOTYPES */\n');
  fh.write('static void bbos_loop();\n');
  fh.write('\n')

  fh.write('static void bbos_init() {\n')
  #fh.write('  BBOS_SET_NR_THREADS(%d);\n' % os.kernel.get_num_threads())
  #fh.write('  BBOS_KERNEL_SET_RUNNING_TYPE(%d);\n' % 0)
  fh.write('}\n')
  fh.write('\n')
  fh.write('static void bbos_start() {\n')
  #fh.write('  bbos_kernel_start();\n')
  fh.write('  bbos_loop();\n')
  fh.write('}\n')
  fh.write('\n')
  fh.write('void main%d(void* arg) {\n' % kernel.get_core().get_id())
  fh.write('  bbos_init();\n')
  fh.write('  bbos_start();\n')
  fh.write('}\n')
  return file_path

def update_bbos_config_h(kernel):
  file_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb", "os", "config_autogen.h")
  fh = open(file_path, 'a')
  for thread in kernel.get_threads():
    fh.write("void %s();\n" % thread.get_runner())
  fh.close()

bb.Builder.rule('bb.os.kernel.kernel.Kernel', {
    'PropellerToolchain': {
      'srcs': (gen_main_c, update_bbos_config_h,)
      }
    })
