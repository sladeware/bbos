#!/usr/bin/python

"""Project page: http://code.google.com/p/propgcc/"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.builder.compilers.unixc import UnixCCompiler

class PropGCCCompiler(UnixCCompiler):
    DEFAULT_EXECUTABLES = {
        "compiler"     : ["propeller-elf-gcc"],
        "linker_exe"   : ["propeller-elf-gcc"]
        }
