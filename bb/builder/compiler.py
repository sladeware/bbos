
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from types import *

from bb.builder.errors import *
from bb.utils.spawn import which, ExecutionError

class Compiler(object):
    """
    Attributes:
    executable: A dictinary of executables."""
    executables = {}

    def __init__(self, verbose=None, dry_run=False):
        self.verbose = verbose
        self.dry_run = dry_run
        # A common output directory for objects, libraries, etc.
        self.output_dir = ""

    def check_executables(self):
        if not self.executables:
            return
        for (name, cmd) in self.executables.items():
            if not which(cmd[0]):
                raise ExecutionError("compiler '%s' can not be found" % cmd[0])

    def get_language(self, *arg_list, **arg_dict):
        raise NotImplemented

    def compile(self, *arg_list, **arg_dict):
        raise NotImplemented

    def get_output_dir(self):
        return self.output_dir

    def set_output_dir(self, output_dir):
        if not output_dir or type(output_dir) is not StringType:
            raise TypeError("'output_dir' must be a string or None")
        else:
            self.output_dir = output_dir

    def _setup_compile(self, output_dir):
        if output_dir is None:
            outputdir = self.output_dir
        elif type(output_dir) is not StringType:
            raise TypeError("'output_dir' must be a string or None")

