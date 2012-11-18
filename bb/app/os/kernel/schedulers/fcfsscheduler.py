#!/usr/bin/env python

from bb.os.kernel.schedulers.dynamicscheduler import DynamicScheduler

class FCFSScheduler(DynamicScheduler):
  """First-Come-First-Served scheduling policy."""
