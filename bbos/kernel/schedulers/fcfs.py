
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.kernel.scheduler import DynamicScheduler

class FCFS(DynamicScheduler):
    """First-Come-First-Served scheduling policy."""
    def __init__(self):
	DynamicScheduler.__init__(self, "FCFS")
    # __init__()


