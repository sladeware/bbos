#!/usr/bin/env python

# import main platform config, MUST be first
import bb.runtime.config as bb_config
from bb.runtime.autogen import bbos_config_autogen

if not bbos_config_autogen:
  print "bbos_config_autogen cannot be imported"
  exit(1)

if not getattr(bb_config, "BB_CONFIG_DEBUG", None):
    setattr(bb_config, "BB_CONFIG_DEBUG", 1)

"""
if cpp.ifndef("BB_CONFIG_DEBUG"):
    cpp.define("BB_CONFIG_DEBUG", True)

if cpp.ifndef("BB_CONFIG_NR_THREADS"):
    cpp.error("Please define BB_CONFIG_NR_THREADS in BB_CONFIG_OS_FILE")
elif BB_CONFIG_NR_THREADS < 1:
    cpp.error("System requires atleast one thread")
"""
#BB_NR_THREADS = BB_CONFIG_NR_THREADS
