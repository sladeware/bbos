
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

class Project:
	"""
	Project.
	"""
	board = None
	processor = None
	core = None

	def __init__(self, board=None, processor=None, core=None):
		if board:
			self.set_board(board)
		self.config_complete = False
		
	def set_board(self, board):
		self.board = board
		self.processor = board.get_processors()[0]
		self.core = self.processor.get_cores()[0]
		self.kernel = self.core.get_process()

	def add_sources(self, sources):
		pass
	
	def add_include_dirs(self, dirs):
		pass

	def config(self):
		"""
		Project configuration includes configuration of board, processor,
		core, kernel and modules.
		"""
		print "Configure project"
		print "Configure board '%s'" % self.board.get_name()
		self.board.config(self)
		print "Configure processor '%s'" % self.processor.get_name()
		self.processor.config(self)
		print "Configure core '%s'" % self.core.get_name()
		self.core.config(self)
		print "Configure process"
		self.kernel.config(self)
		# Configure modules
		for mod in self.kernel.get_modules():
			print "Configure module '%s'" % mod.get_name()
			mod.config()
		self.config_complete = True
	
	def compile(self):
		pass
	
	def load(self):
		pass
	

