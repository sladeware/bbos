
from bb.os.kernel.scheduler import Scheduler

class DynamicScheduler(Scheduler):
    def __init__(self):
        Scheduler.__init__(self) # initialize scheduling interface

