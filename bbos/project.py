
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import time

# The following files will be automatically regenerated each time the project
# will be configured
generated_files = ["bbos.h"]

#_______________________________________________________________________________

class Project:
    """Project base class."""
    board = None
    processor = None
    core = None

    def __init__(self, board=None, processor=None, core=None):
	if board:
	    self.set_board(board)
	self.config_complete = False
	self.sources = []
	self.add_sources(generated_files)
    # __init__()
		
    def set_board(self, board):
	"""Set used board."""
	self.board = board
	self.processor = board.get_processors()[0]
	self.core = self.processor.get_cores()[0]
	self.kernel = self.core.get_process()
    # set_board()

    def add_sources(self, sources):
	self.sources.extend(sources)
    # add_sources()
	
    def get_sources(self):
	"""Get source files."""
	return self.sources
    # get_sources()

    def add_include_dirs(self, dirs):
	pass
    # add_include_dirs()

    def config(self):
	"""Project configuration includes configuration of board, processor,
	core, kernel and modules."""
	# Start to configure project
	print "Configure project"
	# Create files that have to be generated
	for fpath in generated_files:
	    try:
		f = open(fpath, "w")
		print "Create '%s' file" % fpath
	    except IOError:
		print "There were problems creating %s" % fpath
		traceback.print_exc(file=sys.stderr)
		raise
	# Generate the top of bbos.h file
	f = open('bbos.h', 'a')
	f.write("/*\n"
		" * %s\n"
		" *\n"
		" * This is BBOS generated source code used for late binding application\n"
		" * features just before compile time.\n"
		" *\n"
		" * Please do not edit this by hand, as your changes will be lost.\n"
		" *\n"
		" * %s\n"
		" */\n"
		"#ifndef __BBOS_H\n"
		"#define __BBOS_H\n"
		% (time.asctime(), __copyright__))
	f.close()
	# Start to configure board
	print "Configure board '%s'" % self.board.get_name()
	self.board.config(self)
	# Start to configure processor
	print "Configure processor '%s'" % self.processor.get_name()
	self.processor.config(self)
	# Start to configure core
	print "Configure core '%s'" % self.core.get_name()
	self.core.config(self)
	# Start to configure process
	print "Configure process"
	self.kernel.config(self)
	if self.kernel.get_scheduler():
	    print "Configure scheduler '%s'" % self.kernel.scheduler.get_name()
	    self.kernel.get_scheduler().config(self)
	# Start to configure modules
	for mod in self.kernel.get_modules():
	    print "Configure module '%s'" % mod.get_name()
	    mod.config(self)
	# Generate the bottom of the bbos.h
	f = open('bbos.h', 'a')
	f.write("#endif /* __BBOS_H */\n")
	f.close()
	    # Initialization has been completed
	self.config_complete = True
    # config()
	
    def compile(self):
	pass
    # compile()
	
	

