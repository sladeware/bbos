#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.os.kernel.schedulers.scheduler import Scheduler

class StaticScheduler(Scheduler):
    """Static scheduling is widely used with dependable real-time systems
    in application areas such as aerospace and military systems, automotive
    applications, etc.

    In static scheduling, scheduling are made during compile time. This assumes
    parameters of all the tasks is known a priori and builds a schedule based on
    this. Once a schedule is made, it cannot be modified online. Static
    scheduling is generally not recommended for dynamic systems (use dynamic
    scheduler instead).
    """
