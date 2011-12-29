#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This package provides compiler support."""

from bb.builder.compilers.compiler import Compiler
from bb.builder.compilers.c import CCompiler
from bb.builder.compilers.unixc import UnixCCompiler
from bb.builder.compilers.catalina import CatalinaCompiler

SUPPORTED_COMPILERS = {
    'unix': (
        'unixc',
        'UnixCCompiler',
        "standard UNIX-style compiler"
        ),
    'c' : (
        'c',
        'CCompiler',
        ""
        ),
    'catalina' : (
        'catalina',
        'CatalinaCompiler',
        "Catalina is a free ANSI C compiler for the Prallax Propeller"
        ),
    }
"""Contains the list of supported compilers:

   ======================================================= ============================
   Compiler                                                Brief description
   ======================================================= ============================
   :class:`bb.builder.compilers.c.CCompiler`               Standard C-like compiler
   :class:`bb.builder.compilers.unixc.UnixCCompiler`       Standard UNIX-style compiler
   :class:`bb.builder.compilers.catalina.CatalinaCompiler` Catalina compiler
   ======================================================= ============================
"""

def show_compilers():
    """Print list of available compilers."""
    from bb.apps.fancy_getopt import FancyGetopt
    compilers = []
    for compiler in COMPILERS.keys():
        compilers.append(("compiler="+compiler, None,
                          COMPILERS[compiler][2]))
    compilers.sort()
    pretty_printer = FancyGetopt(compilers)
    pretty_printer.print_help("List of available compilers:")
