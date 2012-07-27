#!/usr/bin/env python
######################################################################
# WARNING: this file was automatically generated.
# Do not edit it by hand unless you know what you're doing.
######################################################################
def thread_registration():
  bbos_kernel.register_thread(bbos_config.PRINTER, do_print)

