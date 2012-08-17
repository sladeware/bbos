#!/usr/bin/env python

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import collections

import bb
from bb import Builder

autogen_header = """
//////////////////////////////////////////////////////////////////////
// WARNING: this file was automatically generated.
// Do not edit it by hand unless you know what you're doing.
//////////////////////////////////////////////////////////////////////

"""

autogen_dir_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb")

def gen_os_c(os):
  Builder.context['OS'] = os
  file_path = bb.host_os.path.join(autogen_dir_path, "os", "os_%d_autogen.c" % os.core.get_id())
  fh = open(file_path, 'w')
  fh.write(autogen_header)
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
  fh.write('void main%d(void* arg) {\n' % os.core.get_id())
  fh.write('  bbos_init();\n')
  fh.write('  bbos_start();\n')
  fh.write('}\n')
  return file_path

def gen_config_h(os):
  file_path = bb.host_os.path.join(autogen_dir_path, "os", "config_autogen.h")
  fh = open(file_path, 'a')
  fh.write(autogen_header)
  fh.write("#define BBOS_CONFIG_NR_THREADS %d\n" % os.kernel.get_num_threads())
  for i in range(os.kernel.get_num_threads()):
    thread = os.kernel.get_threads()[i]
    fh.write("#define %s %d\n" % (thread.get_name(), i))
    fh.write("#define %s_RUNNER %s\n" % (thread.get_name(), thread.get_runner()))
  fh.close()

Builder.rule('bb.os.os.OS', {
    'PropellerToolchain' : {
      'srcs': ('kernel.c', gen_os_c, gen_config_h)
      }
})
