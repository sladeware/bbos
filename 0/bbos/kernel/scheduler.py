"""A scheduler is the heart of every RTOS, as it provides the algorithms to 
select the threads for execution."""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
import traceback

from bbos.component import Component
from bbos.kernel.thread import Thread

class Scheduler(Component):
    """Base scheduler class."""
    def __init__(self, name):
	Component.__init__(self, name)
	# __init__()

#_______________________________________________________________________________
		
class StaticScheduler(Scheduler):
    """Static scheduling is widely used with dependable real-time systems 
    in application areas such as aerospace and military systems, automotive 
    applications, etc..

    General moments:
    * Threads execute in a fixed order determined offline
    * Easy to debug but usually give a low processor usage
	
    In static scheduling, scheduling are made during compile time. This assumes 
    parameters of all the tasks is known a priori and builds a schedule based on 
    this. Once a schedule is made, it cannot be modified online. Static 
    scheduling is generally not recommended for dynamic systems (use dynamic 
    scheduler instead)."""
    def __init__(self, name="Basic static scheduler", order=[]):
        Scheduler.__init__(self, name)
        self.set_order(order)
    # __init__()

    def set_order(self, order):
        for thread in order:
            assert isinstance(thread, Thread), \
                "Incorrect order of threads. %s is not a thread" % thread
        self.order = order
    # select_order()

    def get_order(self):
        return self.order
    # get_order()

    def on_build(self, proj):
        # Open bbos.h file
        try:
            f = open(proj.env["bbos.h"], "a")
        except IOError:
            print "There were problems writing to the end of %s" % "bbos.h"
            traceback.print_exc(file=sys.stderr)
            raise
        # Generating scheduling order
        print "Scheduling order: "
        f.write("#define bbos_switch_thread()\\\n")
        f.write("\twhile(1) {\\\n")
        for i in range(len(self.get_order())):
            thread = self.order[i]
            print "\t%d. %s" % (i+1, thread.get_name())
            f.write("\t\t%s();\\\n" % thread.get_entry())
        f.write("\t}\n")
        # Close bbos.h file
        f.close()
    # config()

#_______________________________________________________________________________

class DynamicScheduler(Scheduler):
    def __init__(self, name="Basic dynamic scheduler"):
        Scheduler.__init__(self, name)
    # __init__()

    def _attach(self, proj):
        # Open bbos.h file
        try:
            f = open(proj.env["bbos.h"], "a")
        except IOError:
            print "There were problems writing to the end of %s" % "bbos.h"
            traceback.print_exc(file=sys.stderr)
            raise
        f.write("#define BBOS_SCHED_ENABLED\n")
        # Close bbos.h file
        f.close()
    # config()
