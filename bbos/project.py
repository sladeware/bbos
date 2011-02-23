
class Project:
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
		print "Configure"
		self.kernel.config(self)
	
	def compile(self):
		pass
	
	def load(self):
		pass
	

