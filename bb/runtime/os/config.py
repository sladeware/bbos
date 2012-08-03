#!/usr/bin/env python

import logging

# import main platform config, MUST be first
import bb.runtime.config as bb_config

BBOS_CONFIG_NR_THREADS = 0

import bb.runtime.os.config_autogen

#try:
#  from bb.config_autogen import *
#except ImportError, e:
#  logging.error("bbos_config_autogen cannot be imported."
#                "Maybe you forgot to generate it.")
#  exit(1)

if BBOS_CONFIG_NR_THREADS is None:
  logging.error("Please define BBOS_CONFIG_NR_THREADS in BBOS_CONFIG_FILE")
  exit(0)
elif BBOS_CONFIG_NR_THREADS < 1:
  logging.error("System requires atleast one thread: BBOS_CONFIG_NR_THREADS=0")
  exit(0)
BBOS_NR_THREADS = BBOS_CONFIG_NR_THREADS
