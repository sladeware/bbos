#!/usr/bin/env python

from bb import builder

class OSBuildListener(builder.Listener):
    def on_init(self, os):
        self.autogen_dir_path = host_os.path.join(host_os.environ["BB_HOME"],
                                            "bb", "runtime", "autogen")
        self._gen_bb_config(os)
        self._gen_bb_os(os)

    def _gen_bb_config(self, os):
        file_path = host_os.path.join(self.autogen_dir_path, "bb_config_autogen.py")
        self.add_file(file_path)
        fh = open(file_path, "w")
        fh.write("BB_CONFIG_NR_THREADS = %d\n" % os.microkernel.get_num_threads())
        fh.close()

    def _gen_bb_os(self, os):
        file_path = host_os.path.join(dir_path, "bb_os_autogen.py")
        self.add_file(file_path)
        fh = open(file_path, "w")
        fh.write("import sys\n")
        fh.write("\n")
        fh.write("import bb.runtime.os.os as bb_os\n")
        fh.write("\n")
        fh.write("def thread_registration():\n")
        for thread in os.microkernel.get_threads():
            fh.write("  bb_kernel.register_thread(%s, %s)\n" % (thread.get_name(), thread.get_runner()))
        fh.write("\n")
        fh.write("bb_os = sys.modules['bb.runtime.os.os']\n")
        fh.write("setattr(bb_os, 'thread_registration', thread_registration)\n")
        fh.close()

builder.rule('OS', cases = {
    'SimulationToolchain' : {
      'srcs' : ("./__init__.py", "./os.py", "./../autogen/__init__.py",
                "./../__init__.py", "./../main.py"),
      'lsnr' : (OSBuildListener(),)
      }
    }
               )
