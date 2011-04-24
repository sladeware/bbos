
from types import *

from builder.errors import *

#_______________________________________________________________________________

class Compiler(object):
    executables = {}

    def __init__(self, verbose=False, dry_run=False):
	self.verbose = verbose
	self.dry_run = dry_run
	# A common output directory for objects, libraries, etc.
	self.output_dir = None
    # __init__()

    def get_language(self, *arg_list, **arg_dict):
        raise NotImplemented
    # get_language()

    def compile(self, *arg_list, **arg_dict):
        raise NotImplemented
    # compile()

    def set_output_dir(self, output_dir):
        if not output_dir or type(output_dir) is not StringType:
            raise TypeError, "'output_dir' must be a string or None"
        else:
            self.output_dir = output_dir
    # set_output_dir()

    def _setup_compile(self, output_dir):
	if output_dir is None:
	    outputdir = self.output_dir
	elif type(output_dir) is not StringType:
	    raise TypeError, "'output_dir' must be a string or None"
    # _setup_compile()

# class Compiler
