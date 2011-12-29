#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This package provides compiler support."""

import os
import re
import sys

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

DEFAULT_CCOMPILERS = (
    # Platform string mappings

    # on a cygwin built python we can use gcc like an ordinary UNIXish
    # compiler
    ('cygwin.*', UnixCCompiler),
    ('os2emx', 'emx'),

    # OS name mappings
    ('posix', UnixCCompiler),
    ('nt', 'msvc'),
    ('mac', 'mwerks'),
    )
"""Map a platform/os (``sys.platform``/``os.name``) (e.g. 'posix',
'nt') to the default compiler type for that platform. Keys are
interpreted as re match patterns. Note, order is important; platform
mappings are preferred over OS names."""

def get_default_ccompiler(osname=None, platform=None):
    """Determine the default compiler to use for the given `platform`.

    `osname` should be one of the standard Python OS names (i.e. the
    ones returned by os.name) and platform the common value
    returned by ``sys.platform`` for the platform in question.

    The default values are os.name and ``sys.platform`` in case the
    parameters are not given."""
    if osname is None:
        osname = os.name
    if platform is None:
        platform = sys.platform
    for pattern, compiler in DEFAULT_CCOMPILERS:
        if re.match(pattern, platform) is not None or \
                re.match(pattern, osname) is not None:
            return compiler
    # Default to Unix compiler
    return UnixCCompiler

def new_ccompiler(platform=None, verbose=None, dry_run=False, force=False):
    """Factory function to generate an instance of some
    :class:`bb.builder.compilers.c.CCompiler` subclass for the
    supplied platform/compiler combination. `platform` defaults to
    ``os.name`` (eg. 'posix', 'nt'), and compiler defaults to the default
    compiler for that platform."""
    if platform is None:
        platform = os.name
    try:
        compiler_class = get_default_ccompiler(platform)
    except KeyError:
        msg = "don't know how to compile C/C++ code on platform '%s'" % platform
        raise BuilderPlatformError(msg)
    except KeyError:
        raise BuilderError("can't compile C/C++ code: unable to find class '%s' " 
                           + "in module '%s'") % (class_name, module_name)
    # XXX The None is necessary to preserve backwards compatibility
    # with classes that expect verbose to be the first positional argument.
    return compiler_class(verbose, dry_run)
