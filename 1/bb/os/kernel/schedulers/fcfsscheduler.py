
from bb.os.kernel.schedulers.dynamicscheduler import DynamicScheduler

class FCFSScheduler(DynamicScheduler):
    """First-Come-First-Served scheduling policy."""
    def __init__(self):
        DynamicScheduler.__init__(self, "FCFS")
        self.schedule = []
        self.myself = 'BBOS_IDLE'

    def get_next_thread(self):
        return self.myself

    def move(self):
        idx = self.schedule.index(self.get_next_thread())
        if (idx + 1) >= len(self.schedule):
            idx = 0
        else:
            idx += 1
        self.myself = self.schedule[idx]
        return self.get_next_thread()

    def enqueue(self, thread):
        try:
            if self.schedule.index(thread.get_name()):
                raise
        except:
            pass
        self.schedule.append(thread.get_name())

    def dequeue(self, thread):
        pass
