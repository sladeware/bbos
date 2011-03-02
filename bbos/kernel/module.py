
from bbos.component import Component

class Module(Component):
	def __init__(self, name):
		self.name = name

	def get_name(self):
		return self.name


