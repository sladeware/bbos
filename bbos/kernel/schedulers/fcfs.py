
from bbos.kernel.scheduler import Scheduler

class FCFS(Scheduler):
	"""
	First-Come-First-Served scheduling policy.
	"""
	def __init__(self):
		Scheduler.__init__(self, "FCFS")


