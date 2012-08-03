#!/usr/bin/env python

import bb
from bb import builder
from bb.config import host_os

autogen_header = """
//////////////////////////////////////////////////////////////////////
// WARNING: this file was automatically generated.
// Do not edit it by hand unless you know what you're doing.
//////////////////////////////////////////////////////////////////////

"""

autogen_dir_path = host_os.path.join(bb.env["BB_HOME"], "bb")

def gen_main_c(os):
  file_path = host_os.path.join(autogen_dir_path, "os", "main_autogen.c")
  fh = open(file_path, "w")
  fh.write(autogen_header)
  fh.write("#include <bb/os.h>\n\n")
  fh.write("int main() {\n")
  fh.write("  bbos();\n")
  fh.write("  return 0;\n")
  fh.write("}\n")
  return file_path

def gen_config_h(os):
  file_path = host_os.path.join(autogen_dir_path, "os", "config_autogen.h")
  fh = open(file_path, "w")
  fh.write(autogen_header)
  fh.write("#define BBOS_CONFIG_NR_THREADS %d\n" % os.kernel.get_num_threads())
  for i in range(len(os.kernel.get_threads())):
    thread = os.kernel.get_threads()[i]
    fh.write("#define %s %d\n" % (thread.get_name(), i))
    fh.write("#define %s_RUNNER %s\n" % (thread.get_name(), thread.get_runner()))
  fh.close()

builder.rule('bb.os.os.OS', {
    'PropellerToolchain' : {
      'srcs': ('../os.c', 'kernel.c', gen_main_c, gen_config_h)
      }
})
