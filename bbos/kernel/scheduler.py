
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os

from bbos.component import Component

class Scheduler(Component):
	"""
	A scheduler is the heart of every RTOS, as it provides the algorithms to 
	select the threads for execution.
	"""
	def __init__(self, name):
		Component.__init__(self, name)
		
	def _config(self, proj):
		proj.add_include_dirs(['.', os.path.join(os.environ['BBOSHOME'], 'bbos')])


