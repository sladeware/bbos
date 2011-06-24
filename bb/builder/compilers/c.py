
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os, re, sys, string
import os.path
from types import *

from bb.apps.utils.dir import mkpath
from bb.builder.compiler import Compiler
from bb.builder.errors import *

#_______________________________________________________________________________

# Map a sys.platform/os.name ('posix', 'nt') to the default compiler
# type for that platform. Keys are interpreted as re match
# patterns. Order is important; platform mappings are preferred over OS names.
_default_compilers = (
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
# get_default_compiler()

#_______________________________________________________________________________

# Map compiler types to (module_name, class_name) pairs -- ie. where to
# find the code that implements an interface to this compiler.  (The module
# is assumed to be in the 'distutils' package.)
compiler_class = {
    'unix': (
        'unixc', 
        'UnixCCompiler', 
        "standard UNIX-style compiler"
        )
    }

def new_ccompiler(platform=None, compiler=None, verbose=False, dry_run=False, 
		  force=False):
    if platform is None:
        platform = os.name
    try:
        if compiler is None:
            compiler = get_default_compiler(platform)
        (module_name, class_name, long_description) = compiler_class[compiler]
    except KeyError:
        msg = "don't know how to compile C/C++ code on platform '%s'" % platform
        if compiler is not None:
            msg = msg + " with '%s' compiler" % compiler
        raise BuilderPlatformError, msg
    try:
        module_name = "bb.builder.compilers." + module_name
        __import__(module_name)
        module = sys.modules[module_name]
        klass = vars(module)[class_name]
    except ImportError:
        raise BuilderError, \
            "can't compile C/C++ code: unable to load module '%s'" % \
            module_name
    except KeyError:
        raise BuilderError, \
            ("can't compile C/C++ code: unable to find class '%s' " +
             "in module '%s'") % (class_name, module_name)
    # XXX The None is necessary to preserve backwards compatibility
    # with classes that expect verbose to be the first positional argument.
    return klass(verbose, dry_run)
# new_ccompiler()

#_______________________________________________________________________________

class CCompiler(Compiler):
    """Abstract base class to define the interface of the standard C compiler 
    that must be implemented by real compiler class.

    The basic idea behind a compiler abstraction class is that each instance 
    can be used for all the compiler/link steps in building a single project. 
    Thus, we have an attributes common to all of those compile and link steps --
    include directories, macros to define, libraries to link against, etc. -- 
    are attributes to the compiler instance."""

    source_extensions = None # list of strings
    object_extension = None

    # Default language settings. 
    # language_map is used to detect a source file target language, checking 
    # source filenames.
    # language_order is used to detect the language precedence, when deciding
    # what language to use when mixing source types. For example, if some
    # extension has two files with ".c" extension, and one with ".cpp", it
    # is still linked as c++.
    language_map = {".c"   : "c",
                    ".cc"  : "c++",
                    ".cpp" : "c++",
                    ".cxx" : "c++",
                    ".m"   : "objc",
                   }
    language_order = ["c++", "objc", "c"]

    def __init__(self, verbose=False, dry_run=False):
	Compiler.__init__(self, verbose, dry_run)
	# A list of macro definitions (we are using list since the order is 
        # important). A macro definition is a 2-tuple 
	# (name, value), where the value is either a string or None.
	# A macro undefinition is a 1-tuple (name, ).
	self.macros = []
	# A list of directories
	self.include_dirs = []
        # A list of library names (not filenames: eg. "foo" not "libfoo.a") to 
        # include in any link
	self.libraries = []
	# A list of directories to seach for libraries
        self.library_dirs = []
	# A list of object files
	self.objects = []
    # __init__()

    def _find_macro(self, name):
        """Return position of the macro 'name' in the list of macros."""
        i = 0
        for macro in self.macros:
            if macro[0] == name:
                return i
            i += 1
        return None
    # _find_macro()

    def add_include_dirs(self, dirs):
        """Add a list of dirs 'dirs' to the list of directories that will be
        searched for header files. See add_include_dir()."""
        if type(dirs) is ListType:
            for dir in dirs:
                self.add_include_dir(dir)
        else:
            raise TypeError

    def get_include_dirs(self):
        return self.include_dirs

    def add_include_dir(self, dir):
        """Add 'dir' to the list of directories that will be searched for
        header files. The compiler is instructed to search directories in
        the order in which they are supplied by successive calls to
        'add_include_dir()'."""
        self.include_dirs.append(dir)

    def add_library(self, library_name):
        """Add 'library_name' to the list of libraries that will be included in
        all links driven by this compiler object. Note that 'library_name'
        should *not* be the name of a file containing a library, but the
        name of the library itself: the actual filename will be inferred by
        the linker, the compiler, or the compiler class (depending on the
        platform).

        The linker will be instructed to link against libraries in the
        order they were supplied to 'add_library()' and/or
        'set_libraries()'. It is perfectly valid to duplicate library
        names; the linker will be instructed to link against libraries as
        many times as they are mentioned."""
        self.libraries.append(library_name)
    # add_library()

    def add_libraries(self, libraries):
        if libraries and type(libraries) in (ListType, TupleType):
            for library in list(libraries):
                self.add_library(library)
            libraries = list (libraries) + (self.libraries or [])
        else:
            raise TypeError, \
                "'libraries' (if supplied) must be a list of strings"
    # add_libraries()

    def add_library_dir(self, library_dir):
        """Add 'library_dir' to the list of directories that will be searched 
        for libraries specified to 'add_library()' and 'set_libraries()'. The
        linker will be instructed to search for libraries in the order they
        are supplied to 'add_library_dir()' and/or 'set_library_dirs()'."""
        self.library_dirs.append(library_dir)
    # add_library_dir()

    def add_library_dirs(self, library_dirs):
        if library_dirs and type(library_dirs) in (ListType, TupleType):
            for library_dir in list(library_dirs):
                self.add_library_dir(library_dir)
        else:
            raise TypeError, \
                "'library_dirs' (if supplied) must be a list of strings"
    # add_library_dirs()

    def add_link_object(self, obj):
        """Add 'object' to the list of object files (or analogues, such as
        explicitly named library files or the output of "resource
        compilers") to be included in every link driven by this compiler
        object."""
        self.objects.append(obj)
    # add_link_object()

    def add_link_objects(self, objects):
        """See add_link_object()."""
        if type(objects) not in (ListType, TupleType):
            raise TypeError, \
                "'objects' must be a list or tuple of strings"
        for obj in list(objects):
            self.add_link_object(obj)
    # add_link_objects()

    def define_macro(self, name, value=None):
        """Define a preprocessor macro for all compilations driven by this
        compiler object. The optional parameter 'value' should be a
        string; if it is not supplied, then the macro will be defined
        without an explicit value and the exact outcome depends on the
        compiler used (XXX true? does ANSI say anything about this?)"""
        # Delete from the list of macro definitions/undefinitions if
        # already there (so that this one will take precedence).
        i = self._find_macro(name)
        if i is not None:
            del self.macros[i]
        defn = (name, value)
        self.macros.append(defn)
    # define_macro()

    def get_language(self, sources):
        """Detect the language of a given file, or list of files. Uses
        language_map, and language_order to do the job."""
        if type(sources) is not ListType:
            sources = [sources]
        lang = None
        index = len(self.language_order)
        for source in sources:
            base, ext = os.path.splitext(source)
            extlang = self.language_map.get(ext)
            try:
                extindex = self.language_order.index(extlang)
                if extindex < index:
                    lang = extlang
                    index = extindex
            except ValueError:
                pass
        return lang
    # get_language()

    def get_library_dir_option(self, dir):
        """Return the compiler option to add 'dir' to the list of
        directories searched for libraries."""
        raise NotImplemented
    # get_library_dir_option()

    def get_library_option (self, lib):
        """Return the compiler option to add 'dir' to the list of libraries
        linked into the shared library or executable."""
        raise NotImplementedError
    # get_library_option()

    def find_library_file (self, dirs, lib, debug=0):
        """Search the specified list of directories for a static or shared
        library file 'lib' and return the full path to that file.  If
        'debug' true, look for a debugging version (if that makes sense on
        the current platform).  Return None if 'lib' wasn't found in any of
        the specified directories."""
        raise NotImplementedError
    # find_library_file()

    def _gen_lib_options(self, library_dirs, libraries):
        """Generate linker options for searching library directories and
        linking with specific libraries.  'libraries' and 'library_dirs' are,
        respectively, lists of library names (not filenames!) and search
        directories.  Returns a list of command-line options suitable for use
        with some compiler (depending on the two format strings passed in)."""
        lib_options = []

        for dir in library_dirs:
            lib_options.append(self.get_library_dir_option(dir))

        # XXX it's important that we *not* remove redundant library mentions!
        # sometimes you really do have to say "-lfoo -lbar -lfoo" in order to
        # resolve all symbols.  I just hope we never have to say "-lfoo obj.o
        # -lbar" to get things to work -- that's certainly a possibility, but a
        # pretty nasty way to arrange your C code.

        for lib in libraries:
            (lib_dir, lib_name) = os.path.split(lib)
            if lib_dir:
                lib_file = self.find_library_file([lib_dir], lib_name)
                if lib_file:
                    lib_options.append(lib_file)
                else:
                    self.warn("no library file corresponding to "
                                  "'%s' found (skipping)" % lib)
            else:
                lib_options.append(self.get_library_option(lib))

        return lib_options
    # _get_lib_options()

    def _gen_preprocess_options(self, macros, include_dirs):
	pp_options = []
	for macro in macros:
	    if not (type(macro) is TupleType and 1 <= len (macro) <= 2):
		raise TypeError, \
		    ("bad macro definition '%s': " +
		     "each element of 'macros' list must be a 1- or 2-tuple") %  \
		     macro
	    if len (macro) == 1: # undefine this macro
		pp_options.append ("-U%s" % macro[0])
	    elif len (macro) == 2:
		if macro[1] is None: # define with no explicit value
		    pp_options.append ("-D%s" % macro[0])
		else:
		    # XXX *don't* need to be clever about quoting the
		    # macro value here, because we're going to avoid the
		    # shell at all costs when we spawn the command!
		    pp_options.append ("-D%s=%s" % macro)

	for dir in include_dirs:
	    pp_options.append ("-I%s" % dir)

	return pp_options
    # _gen_preprocess_options()

    def _gen_cc_options(self, pp_options, debug, before):
        cc_opts = pp_options + ['-c']
        if debug:
            cc_opts[:0] = ['-g']
        if before:
            cc_opts[:0] = before
        return cc_opts
    # get_cc_options

    def _gen_ld_options(self, debug, before):
        ld_opts = []
        if debug:
            ld_opts[:0] = ['-g']
        if before:
            ld_opts[:0] = before
        return ld_opts
    # _gen_ld_opts

    def get_object_filenames(self, src_filenames, output_dir=""):
	if output_dir is None:
	    output_dir = ""
	obj_filenames = []
	for src_filename in src_filenames:
	    base, ext = os.path.splitext(src_filename)
	    base = os.path.splitdrive(base)[1]
	    base = base[os.path.isabs(base):]
	    if ext not in self.source_extensions:
		raise UnknownFileError, "unknonw file type '%s' (from '%s')" \
		    % (ext, src_filename)
	    obj_filenames.append(os.path.join(output_dir, \
						  base + self.object_extension))
	return obj_filenames
    # get_object_filenames()

    def compile(self, sources, output_dir=None, macros=None, include_dirs=None,
                debug=0, extra_preopts=None, extra_postopts=None, depends=None):
        macros, objects, extra_postopts, pp_options, build = \
	    self._setup_compile(sources, output_dir, macros, include_dirs, extra_postopts, depends)
	cc_options = self._gen_cc_options(pp_options, debug, extra_preopts)

        for obj in objects:
            try:
                src, ext = build[obj]
            except KeyError:
                continue
            print "Compiling:", src
            self._compile(obj, src, ext, cc_options, extra_postopts, pp_options)
	
	return objects
    # compile()

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        """Compile source to product objects."""
	raise NotImplemented
    # _compile()

    def _setup_compile(self, sources, output_dir, macros, include_dirs, extra, 
		       depends):
        """Process arguments and decide which source files to compile."""
	if output_dir is None:
	    outputdir = self.output_dir
	elif type(output_dir) is not StringType:
	    raise TypeError, "'output_dir' must be a string or None"

        if macros is None:
            macros = self.macros
        elif type(macros) is ListType:
            macros = macros + (self.macros or [])
        else:
            raise TypeError, "'macros' (if supplied) must be a list of tuples"

        if include_dirs is None:
            include_dirs = self.include_dirs
        elif type(include_dirs) in (ListType, TupleType):
            include_dirs = list(include_dirs) + (self.include_dirs or [])
        else:
            raise TypeError, \
                  "'include_dirs' (if supplied) must be a list of strings"

	if extra is None:
	    extra = []

	# List of expected output files
	objects = self.get_object_filenames(sources, output_dir)
	assert len(objects) == len(sources)
	
	pp_options = self._gen_preprocess_options(macros, include_dirs)

	build = {}
	for i in range(len(sources)):
	    src = sources[i]
	    obj = objects[i]
	    ext = os.path.splitext(src)[1]
	    mkpath(os.path.dirname(obj), 0777)
	    build[obj] = (src, ext)
	
	return macros, objects, extra, pp_options, build
    # _setup_compile()

    def link(self, objects, output_filename, *list_args, **dict_args):
        print "Linking executable:", os.path.relpath(output_filename, self.output_dir)
        self._link(objects, output_filename, *list_args, **dict_args)

    def _link(self, objects, output_filename, output_dir=None, debug=False, 
	     extra_preargs=None, extra_postargs=None, target_lang=None):
        raise NotImplementedError

    def _setup_link(self, objects, output_dir, libraries, library_dirs):
        """Typecheck and fix up some of the arguments supplied to the
        class of link methods.  Specifically: ensure that all arguments are
        lists, and augment them with their permanent versions
        (eg. 'self.libraries' augments 'libraries').  Return a tuple with
        fixed versions of all arguments."""
        if type (objects) not in (ListType, TupleType):
            raise TypeError, \
                "'objects' must be a list or tuple of strings"
        objects = list(objects)

        if output_dir is None:
            output_dir = self.output_dir
        elif type (output_dir) is not StringType:
            raise TypeError, "'output_dir' must be a string or None"

        if libraries is None:
            libraries = self.libraries
        elif type(libraries) in (ListType, TupleType):
            libraries = list(libraries) + (self.libraries or [])
        else:
            raise TypeError, \
                "'libraries' (if supplied) must be a list of strings"

        if library_dirs is None:
            library_dirs = self.library_dirs
        elif type (library_dirs) in (ListType, TupleType):
            library_dirs = list (library_dirs) + (self.library_dirs or [])
        else:
            raise TypeError, \
                "'library_dirs' (if supplied) must be a list of strings"

        return objects, output_dir, libraries, library_dirs
    # _setup_link()

# class CCompiler
