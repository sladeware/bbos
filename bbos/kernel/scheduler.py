
import os
from bbos.config import Configurable

class Scheduler(Configurable):
	"""
	A scheduler is the heart of every RTOS, as it provides the algorithms to 
	select the threads for execution.
	"""
	def __init__(self):
		pass
		
	def _config(self, proj):
		proj.add_include_dirs(['.', os.path.join(os.environ['BBOSHOME'], 'bbos')])


