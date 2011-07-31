#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""Supported compilers"""

# Map compiler types to (module_name, class_name, long_description) pairs -- ie.
# where to find the code that implements an interface to this compiler. (The 
# module is assumed to be in the 'bb.builder.compilers' package.)
COMPILERS = {
    'unix': (
        'unixc', 
        'UnixCCompiler', 
        "standard UNIX-style compiler"
        ),
    'c' : (
        'c',
        'CCompiler',
        "standard C-like compiler"
        ),
    'catalina' : (
        'catalina',
        'CatalinaCompiler',
        "Catalina is a free ANSI C compiler for the Prallax Propeller"
        ),
    }

# Map a sys.platform/os.name ('posix', 'nt') to the default compiler
# type for that platform. Keys are interpreted as re match
# patterns. Order is important; platform mappings are preferred over OS names.
DEFAULT_COMPILERS = (
    # Platform string mappings

    # on a cygwin built python we can use gcc like an ordinary UNIXish
    # compiler
    ('cygwin.*', 'unix'),
    ('os2emx', 'emx'),

    # OS name mappings
    ('posix', 'unix'),
    ('nt', 'msvc'),
    ('mac', 'mwerks'),
    )

# Import compilers from bb.builder.compilers package. This replaces the 
# following requirement:
#
#   from bb.builder.compilers.c import CCompiler
#   from bb.builder.compilers.unixc import UnixCCompiler
#   from bb.builder.compilers.catalina import CatalinaCompiler
#
for (module_name, class_name, long_description) in COMPILERS.values():
    module_name = "bb.builder.compilers." + module_name
    module = __import__(module_name, globals(), locals(), [class_name], -1)
    locals()[class_name] = getattr(module, class_name)

#_______________________________________________________________________________

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

def get_default_compiler(osname=None, platform=None):
    """Determine the default compiler to use for the given platform.

    osname should be one of the standard Python OS names (i.e. the
    ones returned by os.name) and platform the common value
    returned by sys.platform for the platform in question.
    
    The default values are os.name and sys.platform in case the
    parameters are not given."""
    if osname is None:
        osname = os.name
    if platform is None:
        platform = sys.platform
    for pattern, compiler in _default_compilers:
        if re.match(pattern, platform) is not None or \
                re.match(pattern, osname) is not None:
            return compiler
    # Default to Unix compiler
    return 'unix'

def new_compiler(platform=None, compiler=None, verbose=None, dry_run=False, 
                 force=False):
    """Factory function to generate an instance of some Compiler subclass for 
    the supplied platform/compiler combination. platform defaults to os.name 
    (eg. 'posix', 'nt'), and compiler defaults to the default compiler for that 
    platform."""
    if platform is None:
        platform = os.name
    try:
        if compiler is None:
            compiler = get_default_compiler(platform)
        (module_name, class_name, long_description) = _compiler_classes[compiler]
    except KeyError:
        msg = "don't know how to compile C/C++ code on platform '%s'" % platform
        if compiler is not None:
            msg = msg + " with '%s' compiler" % compiler
        raise BuilderPlatformError(msg)
    try:
        module_name = "bb.builder.compilers." + module_name
        __import__(module_name)
        module = sys.modules[module_name]
        klass = vars(module)[class_name]
    except ImportError:
        raise BuilderError("can't compile C/C++ code: unable to load module '%s'" 
                           % module_name)
    except KeyError:
        raise BuilderError("can't compile C/C++ code: unable to find class '%s' " 
                           + "in module '%s'") % (class_name, module_name)
    # XXX The None is necessary to preserve backwards compatibility
    # with classes that expect verbose to be the first positional argument.
    return klass(verbose, dry_run)

