
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component

class Module(Component):
	def __init__(self, name):
		Component.__init__(self, name)

	def get_thread(self):
		"""
		Get the thread object relaed to the module.
		"""
		pass

	def get_messages(self):
		"""
		Get the messages related to the module.
		"""
		pass




