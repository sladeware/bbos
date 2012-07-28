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

def gen_config_header(os):
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
      'srcs': ('kernel.c', gen_config_header)
      }
})
