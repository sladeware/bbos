#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from types import *

from bb.builder.errors import *
from bb.utils.spawn import which, ExecutionError

class Compiler(object):
    """The basic compiler class."""

    DEFAULT_EXECUTABLES = dict()
    """Default executables."""

    def __init__(self, verbose=None, dry_run=False):
        self.verbose = verbose
        self.dry_run = dry_run
        # A common output directory for objects, libraries, etc.
        self.output_dir = ""
        self.__executables = dict()
        self.set_executables(self.DEFAULT_EXECUTABLES)

    def set_executables(self, **args):
        """Define the executables (and options for them) that will be run
        to perform the various stages of compilation. The exact set of
        executables that may be specified here depends on the compiler
        class (via the :const:`Compiler.DEFAULT_EXECUTABLES` class attribute).
        For example they may have the following view:

        * `compiler` --- the C/C++ compiler
        * `linker_so` --- linker used to create shared objects and libraries
        * `linker_exe` --- linker used to create binary executables
        * `archiver` --- static library creator

        On platforms with a command-line (Unix, DOS/Windows), each of these
        is a string that will be split into executable name and (optional)
        list of arguments. (Splitting the string is done similarly to how
        Unix shells operate: words are delimited by spaces, but quotes and
        backslashes can override this. See
        'distutils.util.split_quoted()'.)"""

        # Note that some CCompiler implementation classes will define class
        # attributes 'cpp', 'cc', etc. with hard-coded executable names;
        # this is appropriate when a compiler class is for exactly one
        # compiler/OS combination (eg. MSVCCompiler).  Other compiler
        # classes (UnixCCompiler, in particular) are driven by information
        # discovered at run-time, since there are many different ways to do
        # basically the same things with Unix C compilers.
        for key in args.keys():
            if key not in self.executables:
                raise ValueError, \
                      "unknown executable '%s' for class %s" % \
                      (key, self.__class__.__name__)
            self.set_executable(key, args[key])

    def set_executable(self, key, value):
        """Define the executable (and options for it) that will be run
        to perform some compilation stage."""
        if isinstance(value, str):
            setattr(self, key, split_quoted(value))
        else:
            setattr(self, key, value)

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

def register_compiler(compiler):
    pass
