
import os
from bbos.config import Configurable

class Scheduler(Configurable):
	def __init__(self):
		pass
		
	def _config(self, proj):
		proj.add_include_dirs(['.', os.path.join(os.environ['BBOSHOME'], 'bbos')])


