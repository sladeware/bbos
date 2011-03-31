
import os, string, sys
from types import *

try:
    import warnings
except ImportError:
    warnings = None

#_______________________________________________________________________________

class Extension:
    """Just a collection of attributes that describes an extension
    module and everything needed to build it (hopefully in a portable
    way, but there are hooks that let you be as unportable as you need).
    """

    # When adding arguments to this constructor, be sure to update
    # setup_keywords in core.py.
    def __init__ (self, name, sources,
                  include_dirs=None,
                  define_macros=None,
                  undef_macros=None,
                  library_dirs=None,
                  libraries=None,
                  runtime_library_dirs=None,
                  extra_objects=None,
                  extra_compile_args=None,
                  extra_link_args=None,
                  export_symbols=None,
                  swig_opts = None,
                  depends=None,
                  language=None,
                  **kw                      # To catch unknown keywords
                 ):
        assert type(name) is StringType, "'name' must be a string"
        assert (type(sources) is ListType and
                map(type, sources) == [StringType]*len(sources)), \
                "'sources' must be a list of strings"

        self.name = name
        self.sources = sources
        self.include_dirs = include_dirs or []
        self.define_macros = define_macros or []
        self.undef_macros = undef_macros or []
        self.library_dirs = library_dirs or []
        self.libraries = libraries or []
        self.runtime_library_dirs = runtime_library_dirs or []
        self.extra_objects = extra_objects or []
        self.extra_compile_args = extra_compile_args or []
        self.extra_link_args = extra_link_args or []
        self.export_symbols = export_symbols or []
        self.swig_opts = swig_opts or []
        self.depends = depends or []
        self.language = language

        # If there are unknown keyword options, warn about them
        if len(kw):
            L = kw.keys() ; L.sort()
            L = map(repr, L)
            msg = "Unknown Extension options: " + string.join(L, ', ')
            if warnings is not None:
                warnings.warn(msg)
            else:
                sys.stderr.write(msg + '\n')



