
from bb.os.kernel import Scheduler

#_______________________________________________________________________________

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
        self.__order = []
        self.__cursor = 0

    def get_next_thread(self):
        return self.__order[self.__cursor]

    def enqueue(self, thread):
        self.__order.append(thread)

    def move(self):
        if (self.__cursor + 1) >= len(self.__order):
            self.__cursor = 0
        else:
            self.__cursor += 1
        return self.get_next_thread()

    def get_order(self):
        return self.__order

import bb.os.kernel.schedulers.staticscheduler.setup
