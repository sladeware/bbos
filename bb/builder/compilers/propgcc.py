#!/usr/bin/python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.builder.compilers.unixc import UnixCCompiler

class PropGCCCompiler(UnixCCompiler):
    """PropGCC is a GCC port for the Parallax Propeller P8x32a
    Microcontroller. Project page: http://code.google.com/p/propgcc/"""

    DEFAULT_EXECUTABLES = {
        "compiler"     : ["propeller-elf-gcc"],
        "linker_exe"   : ["propeller-elf-gcc"]
        }
