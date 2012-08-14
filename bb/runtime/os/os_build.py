#!/usr/bin/env python

import bb
from bb import builder

autogen_dir_path = bb.host_os.path.join(bb.env["BB_HOME"], "bb", "runtime")

autogen_header = """#!/usr/bin/env python
######################################################################
# WARNING: this file was automatically generated.
# Do not edit it by hand unless you know what you're doing.
######################################################################
"""

def gen_config_file(os):
  file_path = bb.host_os.path.join(autogen_dir_path, "os", "config_autogen.py")
  fh = open(file_path, "w")
  fh.write(autogen_header)
  fh.write("BBOS_CONFIG_NR_THREADS = %d\n" % os.microkernel.get_num_threads())
  for i in range(len(os.microkernel.get_threads())):
    thread = os.microkernel.get_threads()[i]
    fh.write("%s = %d\n" % (thread.get_name(), i))
    fh.write("%s_RUNNER = %s\n" % (thread.get_name(), thread.get_runner()))
  fh.close()
  return file_path

def gen_os_file(os):
  file_path = bb.host_os.path.join(autogen_dir_path, "os", "os_autogen.py")
  fh = open(file_path, "w")
  fh.write(autogen_header)
  fh.write("def thread_registration():\n")
  for thread in os.microkernel.get_threads():
    fh.write("  bbos_kernel.register_thread(bbos_config.%s, %s)\n" % (thread.get_name(),
                                                        thread.get_runner()))
  fh.write("\n")
  fh.close()
  return file_path

builder.rule('bb.os.os.OS', {
    'SimulationToolchain' : {
      'srcs' : ("./__init__.py", "./os.py",
                "./../__init__.py", "./../main.py",
                gen_config_file, gen_os_file),
      }
    })
