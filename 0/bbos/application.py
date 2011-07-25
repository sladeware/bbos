
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
import time

# The following files will be automatically regenerated each time the project
# will be configured
generated_files = ["bbos.h"]

from builder.project import Extension

#_______________________________________________________________________________

class Application(Extension):
    """Project base class."""
    board = None
    processor = None
    core = None

    def __init__(self, board=None, processor=None, core=None):
        Extension.__init__(self)
	if board:
	    self.set_board(board)
	self.config_complete = False
    # __init__()
		
    def set_board(self, board):
	"""Set used board."""
	self.board = board
	self.processor = board.get_processors()[0]
	self.core = self.processor.get_cores()[0]
	self.kernel = self.core.get_process()
    # set_board()

    def on_build(self, proj):
        pass

    def on_add(self, proj):
        proj.add_sources([self.kernel])

	for mod in self.kernel.get_modules():
	    print "Configuring module '%s'" % mod.get_name()
	    mod.config(self)
            proj.add_source(mod)

    def on_build(self, proj):
	"""Project configuration includes configuration of board, processor,
	core, kernel and modules."""
	# Start to configure project
	print "Configuring application"
	# Create files that have to be generated
	for fpath in generated_files:
            proj.env[fpath] = os.path.join(proj.compiler.get_output_dir(), fpath)
	    try:
		f = open(proj.env[fpath], "w")
		print "Create '%s' file" % proj.env[fpath]
	    except IOError:
		print "There were problems creating %s" % proj.env[fpath]
		traceback.print_exc(file=sys.stderr)
		raise
	# Generate the top of bbos.h file
	f = open(proj.env['bbos.h'], 'a')
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
	print "Configuring board '%s'" % self.board.get_name()
	self.board.config(self)
	# Start to configure processor
	print "Configuring processor '%s'" % self.processor.get_name()
	self.processor.config(self)
	# Start to configure core
	print "Configuring core '%s'" % self.core.get_name()
	self.core.config(self)
	# Start to configure process
	print "Configuring process"
	self.kernel.config(self)
	if self.kernel.get_scheduler():
	    print "Configuring scheduler '%s'" % self.kernel.scheduler.get_name()
	    self.kernel.get_scheduler().config(self)

	# Generate the bottom of the bbos.h
	f = open(proj.env['bbos.h'], 'a')
	f.write("#endif /* __BBOS_H */\n")
	f.close()

        # Initialization has been completed
	self.config_complete = True
    # config()

