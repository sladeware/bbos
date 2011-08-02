
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import collections

from bb.os.kernel import Scheduler

class StaticScheduler(Scheduler):
    """Static scheduling is widely used with dependable real-time systems 
    in application areas such as aerospace and military systems, automotive 
    applications, etc.

    General moments:
    * Threads execute in a fixed order determined offline
    * Easy to debug but usually give a low processor usage
    
    In static scheduling, scheduling are made during compile time. This assumes 
    parameters of all the tasks is known a priori and builds a schedule based on 
    this. Once a schedule is made, it cannot be modified online. Static 
    scheduling is generally not recommended for dynamic systems (use dynamic 
    scheduler instead)."""

    def __init__(self):
        Scheduler.__init__(self)
        self.__order = collections.OrderedDict()
        self.__cursor = 0

    def get_running_thread(self):
        return self.__order.values()[self.__cursor]

    def move(self):
        if (self.__cursor + 1) >= len(self.__order):
            self.__cursor = 0
        else:
            self.__cursor += 1
        # Return new running thread
        return self.get_running_thread()

    def enqueue_thread(self, thread):
        self.__order[id(thread)] = thread

    def dequeue_thread(self, thread):
        del self.__order[id(thread)]


import bb.os.kernel.schedulers.staticscheduler.setup
