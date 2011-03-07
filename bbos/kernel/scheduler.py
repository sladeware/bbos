
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os

from bbos.component import Component

class Scheduler(Component):
	"""
	A scheduler is the heart of every RTOS, as it provides the algorithms to 
	select the threads for execution.
	"""
	def __init__(self, name, is_dynamic=True):
		Component.__init__(self, name)
		self.is_dynamic = is_dynamic
		
	def is_dynamic(self):
		"""
		Defines whether scheduler is dynamic or static.
		"""
		return self.is_dynamic

	def config(self, proj):
		pass
	# config()


