#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import types

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
        self.output_filename = ""
        self.__executables = dict()
        self.set_executables(self.DEFAULT_EXECUTABLES)

    def set_executables(self, *args, **kargs):
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
        if type(args[0]) is types.DictType:
            kargs.update(args[0])
        # Note that some CCompiler implementation classes will define class
        # attributes 'cpp', 'cc', etc. with hard-coded executable names;
        # this is appropriate when a compiler class is for exactly one
        # compiler/OS combination (e.g. MSVCCompiler). Other compiler
        # classes (UnixCCompiler, in particular) are driven by information
        # discovered at run-time, since there are many different ways to do
        # basically the same things with Unix C compilers.
        for key in kargs.keys():
            self.set_executable(key, kargs[key])

    def set_executable(self, key, value):
        """Define the executable (and options for it) that will be run
        to perform some compilation stage."""
        if isinstance(value, str):
            self.__executables[key] = split_quoted(value)
        else:
            self.__executables[key] = value

    def get_executable(self, name):
        """Return executable by its `name`. If it does not exist
        return ``None``."""
        return self.__executables.get(name, None)

    def check_executables(self):
        """Check compiler executables. All of them has to exist. Print
        warning if some executable was specified but not defined."""
        if not self.__executables:
            return
        for (name, cmd) in self.__executables.items():
            if not cmd:
                print "WARNING: undefined executable '%s'" % name
                continue
            if not which(cmd[0]):
                raise ExecutionError("executable '%s' can not be found" % cmd[0])

    def get_language(self, *arg_list, **arg_dict):
        raise NotImplemented

    def compile(self, *arg_list, **arg_dict):
        raise NotImplemented

    def set_output_filename(self, filename):
        """Set output file name."""
        self.output_filename = filename

    def get_output_filename(self):
        """Return output file name."""
        return self.output_filename

    def get_output_dir(self):
        """Return output directory."""
        return self.output_dir

    def set_output_dir(self, output_dir):
        """Set output directory."""
        if not output_dir or type(output_dir) is not types.StringType:
            raise types.TypeError("'output_dir' must be a string or None")
        else:
            self.output_dir = output_dir

    def _setup_compile(self, output_dir):
        if output_dir is None:
            outputdir = self.output_dir
        elif type(output_dir) is not types.StringType:
            raise types.TypeError("'output_dir' must be a string or None")
