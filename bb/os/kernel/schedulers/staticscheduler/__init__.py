__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.os.kernel.scheduler import Scheduler

class StaticScheduler(object, Scheduler):
    """Static scheduling is widely used with dependable real-time systems
    in application areas such as aerospace and military systems, automotive
    applications, etc.

    In static scheduling, scheduling are made during compile time. This assumes
    parameters of all the tasks is known a priori and builds a schedule based on
    this. Once a schedule is made, it cannot be modified online. Static
    scheduling is generally not recommended for dynamic systems (use dynamic
    scheduler instead)."""

    def __init__(self):
        self.__order = []
        self.__cursor = 0

    def get_running_thread(self):
        return self.__order[self.__cursor]

    def move(self):
        if (self.__cursor + 1) >= len(self.__order):
            self.__cursor = 0
        else:
            self.__cursor += 1
        # Return new running thread
        return self.get_running_thread()

    def enqueue_thread(self, thread):
        self.__order.append(thread)

    def dequeue_thread(self, thread):
        pass
        #del self.__order[id(thread)]

    def get_order(self):
        return self.__order

import bb.os.kernel.schedulers.staticscheduler.setup
