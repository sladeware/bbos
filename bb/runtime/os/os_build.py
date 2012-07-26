#!/usr/bin/env python

import bb
from bb import builder
from bb.config import host_os

autogen_dir_path = host_os.path.join(bb.env["BB_HOME"],
                                     "bb", "runtime", "autogen")

def gen_bb_config_file(os):
  file_path = host_os.path.join(autogen_dir_path, "bb_config_autogen.py")
  fh = open(file_path, "w")
  fh.write("BB_CONFIG_NR_THREADS = %d\n" % os.microkernel.get_num_threads())
  fh.close()
  return file_path

def gen_bb_os_file(os):
  file_path = host_os.path.join(autogen_dir_path, "bb_os_autogen.py")
  fh = open(file_path, "w")
  fh.write("import sys\n")
  fh.write("\n")
  fh.write("import bb.runtime.os.os as bb_os\n")
  fh.write("\n")
  fh.write("def thread_registration():\n")
  for thread in os.microkernel.get_threads():
    fh.write("  bb_kernel.register_thread(%s, %s)\n" % (thread.get_name(),
                                                        thread.get_runner()))
  fh.write("\n")
  fh.write("bb_os = sys.modules['bb.runtime.os.os']\n")
  fh.write("setattr(bb_os, 'thread_registration', thread_registration)\n")
  fh.close()
  return file_path

builder.rule('bb.os.os.OS', {
    'SimulationToolchain' : {
      'srcs' : ("./__init__.py", "./os.py", "./../autogen/__init__.py",
                "./../__init__.py", "./../main.py",
                gen_bb_config_file, gen_bb_os_file),
      }
    })
