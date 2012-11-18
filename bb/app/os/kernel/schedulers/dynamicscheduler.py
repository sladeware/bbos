#!/usr/bin/env python

from bb.os.kernel.schedulers.scheduler import Scheduler

class DynamicScheduler(Scheduler):
    def __init__(self):
        Scheduler.__init__(self)
