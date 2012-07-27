#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import sys
import time

from bb.config import host_os
from bb.lib.utils.host_os.path import mkpath

from bb.lib.utils import typecheck
from bb.lib.build.compilers.compiler import Compiler

class Linker(object):
  def __init__(self):
    self._output_dir = ""
    self._output_filename = ""
    self._opts = list()

  def add_opt(self, opt):
    self._opts.append(opt)

  def add_opts(self, opts):
    for opt in opts:
      self.add_opt(opt)

  def get_opts(self):
    return self._opts

  def set_output_filename(self, filename):
    self._output_filename = filename

  def get_output_filename(self):
    return self._output_filename

  def get_output_dir(self):
    return self._output_dir

  def set_output_dir(self, output_dir):
    if not output_dir or not typecheck.is_string(output_dir):
      raise types.TypeError("'output_dir' must be a string or None")
    else:
      self._output_dir = output_dir

  def link(self, objects, output_filename, *list_args, **dict_args):
    # Adopt output file name to output directory
    if self.get_output_dir() is not None:
      self.set_output_filename(host_os.path.join(self.get_output_dir(),
                                                 output_filename))
    print "Linking executable:", host_os.path.relpath(output_filename,
                                                      self.output_dir)
    self._link(objects, *list_args, **dict_args)

class CustomCCompiler(Compiler):
  """Abstract base class to define the interface of the standard C compiler that
  must be implemented by real compiler class.

  The basic idea behind a compiler abstraction class is that each instance can
  be used for all the compiler/link steps in building a single project. Thus, we
  have an attributes common to all of those compile and link steps -- include
  directories, macros to define, libraries to link against, etc. -- are
  attributes to the compiler instance.

  Flags are `verbose` (show verbose output), `dry_run` (don't actually execute
  the steps) and `force` (rebuild everything, regardless of dependencies). All
  of these flags default to ``0`` (off).

  C compiler uses language precedence order to identify the language, when
  deciding what language to use when mixing source types. For example, if some
  extension has two files with ``.c`` extension, and one with ``.cpp``, it is
  still linked as ``c++``. The order can be changed by using
  :func:`CCompiler.set_language_precedence_order`. By default it equals to
  :const:`CCompiler.DEFAULT_LANGUAGE_PRECEDENCE_ORDER`.

  Learn more about GCC options:
  http://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html
  """

  DEFAULT_LANGUAGE_PRECEDENCE_ORDER = ["c++", "objc", "c"]
  """Default language precedence order: ``c++``, ``objc``, ``c``."""

  DEFAULT_SOURCE_EXTENSIONS = None
  """Default source extensions."""

  DEFAULT_OBJECT_EXTENSION = None
  """Default object file extension."""

  DEFAULT_EXT_TO_LANGUAGE_MAPPING = {
    ".c"   : "c",
    ".cc"  : "c++",
    ".cpp" : "c++",
    ".cxx" : "c++",
    ".m"   : "objc",
    }
  """This mapping is used to detect a source file target language, by checking
  thier filenames.

  =========  ========
  Extension  Language
  =========  ========
  .c         c
  .cc        c++
  .cpp       c++
  .cxx       c++
  .m         objc
  =========  ========
  """

  def __init__(self, verbose=0, dry_run=False):
    Compiler.__init__(self, verbose, dry_run)
    # A list of macro definitions (we are using list since the order is
    # important). A macro definition is a 2-tuple (name, value), where
    # the value is either a string or None. A macro undefinition is a
    # 1-tuple (name, ).
    self.macros = list()
    # A list of directories
    self.include_dirs = list()
    # A list of library names (not filenames: eg. "foo" not "libfoo.a")
    # to include in any link
    self.libraries = list()
    # A list of directories to seach for libraries
    self.library_dirs = list()
    # A list of object files
    self.objects = list()
    self._object_extension = None
    self.set_object_extension(self.DEFAULT_OBJECT_EXTENSION)
    self._source_extensions = list()
    self.set_source_extensions(self.DEFAULT_SOURCE_EXTENSIONS)
    self._language_by_ext_mapping = dict()
    self.set_ext_to_language_mapping(self.DEFAULT_EXT_TO_LANGUAGE_MAPPING)
    self._language_precedence_order = list()
    self.set_language_precedence_order(self.DEFAULT_LANGUAGE_PRECEDENCE_ORDER)
    self._extra_preopts = list()
    self._extra_postopts = list()
    self._linker = None

  def show_compilers():
    """Print list of available compilers."""
    from bb.apps.fancy_getopt import FancyGetop
    compilers = []
    for compiler in COMPILERS.keys():
      compilers.append(("compiler="+compiler, None,
                        COMPILERS[compiler][2]))
    compilers.sort()
    pretty_printer = FancyGetopt(compilers)
    pretty_printer.print_help("List of available compilers:")

  def get_default_ccompiler(osname=None, platform=None):
    """Determine the default compiler to use for the given `platform`.

    `osname` should be one of the standard Python OS names (i.e. the ones
    returned by os.name) and platform the common value returned by
    ``sys.platform`` for the platform in question.

    The default values are os.name and ``sys.platform`` in case the
    parameters are not given.
    """
    if osname is None:
      osname = host_os.name
    if platform is None:
      platform = sys.platform
    for pattern, compiler in DEFAULT_CCOMPILERS:
      if re.match(pattern, platform) is not None or \
            re.match(pattern, osname) is not None:
        return compiler
        # Default to Unix compiler
    return UnixCCompiler

  def get_linker(self):
    return self._linker

  def set_linker(self, linker):
    self._linker = linker
    return self._linker

  def set_object_extension(self, ext):
    self._object_extension = ext

  def get_source_extensions(self):
    return self._source_extensions

  def set_source_extensions(self, extensions):
    for ext in extensions:
      self.add_source_extension(ext)

  def add_source_extension(self, extension):
    self._source_extensions.append(extension)

  def bind_ext_to_language(self, extension, language):
    """Maps the given filename `extension` to the specified content
    `language`.
    """
    self._language_by_ext_mapping[extension] = language

  def set_ext_to_language_mapping(self, mapping):
    """Set file extension to language mapping.
    See also :const:`CCompiler.DEFAULT_LANGUAGE_BY_EXT_MAPPING`.
    """
    for ext, language in mapping.items():
      self.bind_ext_to_language(ext, language)

  def get_object_extension(self):
    """Return object file extension."""
    return self._object_extension

  def set_object_extension(self, extension):
    """The `extension` argument is case-insensitive and can be
    specified with or without a leading dot.
    """
    self._object_extension = extension

  def set_language_precedence_order(self, order):
    """Set language precedence order. This order will be used by
    :func:`CCompiler.identify_language` to identify language name. See also
    :const:`CCompiler.DEFAULT_LANGUAGE_PRECEDENCE_ORDER`.
    """
    self._language_precedence_order = order

  def get_language_precedence_order(self):
    """Return language precedence order."""
    return self._language_precedence_order

  def _find_macro(self, name):
    """Return position of the macro 'name' in the list of macros."""
    i = 0
    for macro in self.macros:
      if macro[0] == name:
        return i
      i += 1
    return None

  def add_include_dirs(self, dirs):
    """Add a list of dirs 'dirs' to the list of directories that will be
    searched for header files. See :func:`CCompiler.add_include_dir`.
    """
    if typecheck.is_list(dirs):
      for dir in dirs:
        self.add_include_dir(dir)
    raise TypeError

  def get_include_dirs(self):
    return self.include_dirs

  def add_include_dir(self, dir):
    """Add `dir` to the list of directories that will be searched for header
    files. The compiler is instructed to search directories in the order in
    which they are supplied by successive calls to 'add_include_dir()'.
    """
    self.include_dirs.append(dir)

  def add_library(self, library_name):
    """Add `library_name` to the list of libraries that will be included in all
    links driven by this compiler object. Note that `library_name` should *not*
    be the name of a file containing a library, but the name of the library
    itself: the actual filename will be inferred by the linker, the compiler, or
    the compiler class (depending on the platform).

    The linker will be instructed to link against libraries in the order they
    were supplied to 'add_library()' and/or 'set_libraries()'. It is perfectly
    valid to duplicate library names; the linker will be instructed to link
    against libraries as many times as they are mentioned.
    """
    self.libraries.append(library_name)

  def add_libraries(self, libraries):
    if libraries and typecheck.is_sequence(libraries):
      for library in list(libraries):
        self.add_library(library)
      libraries = list (libraries) + (self.libraries or [])
    else:
      raise TypeError("'libraries' (if supplied) must be a list of strings")

  def add_library_dir(self, library_dir):
    """Add `library_dir` to the list of directories that will be searched for
    libraries specified to :func:`CCompiler.add_library` and
    :func:`CCompiler.set_libraries`. The linker will be instructed to search for
    libraries in the order they are supplied to 'add_library_dir()' and/or
    'set_library_dirs()'."""
    self.library_dirs.append(library_dir)

  def add_library_dirs(self, library_dirs):
    if library_dirs and typecheck.is_sequence(library_dirc):
      for library_dir in list(library_dirs):
        self.add_library_dir(library_dir)
    else:
      raise TypeError("'library_dirs' (if supplied) must be a list of "
                      + "strings")

  def add_link_object(self, obj):
    """Add `obj` to the list of object files (or analogues, such as
    explicitly named library files or the output of "resource
    compilers") to be included in every link driven by this compiler
    object.
    """
    self.objects.append(obj)

  def add_link_objects(self, objects):
    """See :func:`CCompiler.add_link_object`."""
    if typecheck.is_sequence(objects):
      raise TypeError("'objects' must be a list or tuple of strings")
    for obj in list(objects):
      self.add_link_object(obj)

  def define_macro(self, name, value=None):
    """Define a preprocessor macro for all compilations driven by this
    compiler object. The optional parameter `value` should be a
    string; if it is not supplied, then the macro will be defined
    without an explicit value and the exact outcome depends on the
    compiler used (XXX true? does ANSI say anything about this?)
    """
    # Delete from the list of macro definitions/undefinitions if
    # already there (so that this one will take precedence).
    i = self._find_macro(name)
    if i is not None:
      del self.macros[i]
    defn = (name, value)
    self.macros.append(defn)

  def undefine_macro(self, name):
    # Delete from the list of macro definitions/undefinitions if
    # already there
    i = self._find_macro(name)
    if i is not None:
      del self.macros[i]
    undefn = (name, )
    self.macros.append(undefn)

  def identify_language(self, sources):
    """Identify the language of a given file, or list of files. Uses
    language_map, and :func:`CCompiler.get_language_precedence_order`
    to do the job.
    """
    if not typecheck.is_list(sources):
      sources = [sources]
    lang = None
    index = len(self.language_order)
    for source in sources:
      base, ext = host_os.path.splitext(source)
      extlang = self.language_map.get(ext)
      try:
        extindex = self.language_order.index(extlang)
        if extindex < index:
          lang = extlang
          index = extindex
      except ValueError:
        pass
    return lang

  def get_library_dir_option(self, dir):
    """Return the compiler option to add 'dir' to the list of
    directories searched for libraries.
    """
    raise NotImplemented

  def get_library_option (self, lib):
    """Return the compiler option to add 'dir' to the list of libraries
    linked into the shared library or executable.
    """
    raise NotImplementedError

  def find_library_file (self, dirs, lib, debug=0):
    """Search the specified list of directories for a static or shared
    library file `lib` and return the full path to that file. If
    `debug` true, look for a debugging version (if that makes sense on
    the current platform). Return ``None`` if `lib` wasn't found in any of
    the specified directories.
    """
    raise NotImplementedError

  def _gen_lib_options(self, library_dirs, libraries):
    """Generate linker options for searching library directories and
    linking with specific libraries.  'libraries' and 'library_dirs' are,
    respectively, lists of library names (not filenames!) and search
    directories.  Returns a list of command-line options suitable for use
    with some compiler (depending on the two format strings passed in).
    """
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

  def _gen_preprocess_macro_options(self, macros):
    """macros is the usual thing, a list of 1- or 2-tuples, where (name,)
    means undefine (-U) macro 'name', and (name, value) means define (-D)
    macro 'name' to 'value'.
    """
    options = []
    for macro in macros:
      if not (typecheck.is_tuple(macro) and 1 <= len(macro) <= 2):
        raise TypeError("bad macro definition " + repr(macro) + ": " +
                        "each element of 'macros' list must be a 1- or 2-tuple")
      if len (macro) == 1: # undefine this macro
        options.append("-U%s" % macro[0])
      elif len (macro) == 2:
        if macro[1] is None: # define with no explicit value
          options.append("-D%s" % macro[0])
        else:
          # XXX *don't* need to be clever about quoting the
          # macro value here, because we're going to avoid the
          # shell at all costs when we spawn the command!
          options.append("-D%s=%s" % macro)
    return options

  def _gen_preprocess_include_options(self, include_dirs):
    """include_dirs is just a list of directory names to be added to the
    header file search path (-I).
    """
    options = []
    for dir in include_dirs:
      options.append ("-I%s" % dir)
    return options

  def _gen_preprocess_options(self, macros, include_dirs):
    """Generate C pre-processor options(-D, -U, -I) as used by at least two
    types of compilers: the typical Unix compiler and Visual C++. Return
    a list of command-line options suitable for either Unix compilers and
    Visual C++.
    """
    pp_options = self._gen_preprocess_macro_options(macros) \
        + self._gen_preprocess_include_options(include_dirs)
    return pp_options

  def _gen_cc_options(self, pp_options, debug, before):
    cc_opts = pp_options + ['-c']
    if debug:
      cc_opts[:0] = ['-g']
    if before:
      cc_opts[:0] = before
    return cc_opts

  def _gen_ld_options(self, debug, before):
    ld_opts = []
    if debug:
      ld_opts[:0] = ['-g']
    if before:
      ld_opts[:0] = before
    return ld_opts

  def get_object_filenames(self, src_filenames, output_dir=""):
    if output_dir is None:
      output_dir = ""
    obj_filenames = []
    for src_filename in src_filenames:
      base, ext = host_os.path.splitext(src_filename)
      base = host_os.path.splitdrive(base)[1]
      base = base[host_os.path.isabs(base):]
      if ext not in self.get_source_extensions():
        raise UnknownFileError("unknown file type '%s' (from '%s')" \
                                 % (ext, src_filename))
      obj_filenames.append(
        host_os.path.join(output_dir, base + self.get_object_extension()))
    return obj_filenames

  def set_extra_preopts(self, extra_preopts):
    self._extra_preopts = extra_preopts

  def get_extra_preopts(self):
    return self._extra_preopts

  def set_extra_postopts(self, extra_postopts):
    self._extra_postopts = extra_postopts

  def get_extra_postopts(self):
    return self._extra_postopts

  def compile(self, sources, output_dir=None, macros=None, include_dirs=None,
              debug=0, extra_preopts=None, extra_postopts=None, depends=None):
    # Play with extra preopts and postopts
    extra_preopts = self.get_extra_preopts()
    extra_postopts = self.get_extra_postopts()
    # Setup compilation process first
    macros, objects, extra_postopts, pp_options, build = \
        self._setup_compile(sources, output_dir, macros, include_dirs, extra_postopts, depends)
    cc_options = self._gen_cc_options(pp_options, debug, extra_preopts)
    for obj in objects:
      try:
        src, ext = build[obj]
      except KeyError:
        continue
      if self.dry_run:
        print "Compiling:", src
      else:
        sys.stdout.flush()
        sys.stdout.write("Compiling: %s\r" % src)
        time.sleep(0.010)
        # Note: we pass a copy of sources, options, etc. since we
        # need to privent their modification
        self._compile(obj, src, ext, list(cc_options), extra_postopts, pp_options)
    if not self.dry_run:
      print
    return objects

  def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
    """Compile source to product objects."""
    raise NotImplemented

  def _setup_compile(self, sources, output_dir, macros, include_dirs, extra,
                     depends):
    """Process arguments and decide which source files to compile."""
    if output_dir is None:
      outputdir = self.output_dir
    elif not typecheck.is_string(output_dir):
      raise TypeError("'output_dir' must be a string or None")

    if macros is None:
      macros = self.macros
    elif typecheck.is_list(macros):
      macros = macros + (self.macros or [])
    else:
      raise TypeError("'macros' (if supplied) must be a list of tuples")
    if include_dirs is None:
      include_dirs = self.include_dirs
    elif typecheck.is_sequence(include_dirs):
      include_dirs = list(include_dirs) + (self.include_dirs or [])
    else:
      raise TypeError("'include_dirs' (if supplied) must be a list of strings")
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
      ext = host_os.path.splitext(src)[1]
      mkpath(host_os.path.dirname(obj), 0777)
      build[obj] = (src, ext)
    return macros, objects, extra, pp_options, build

  def link(self, objects, output_filename, *list_args, **dict_args):
    """Start linking process."""
    # Adopt output file name to output directory
    if self.get_output_dir() is not None:
      self.set_output_filename(host_os.path.join(self.get_output_dir(), \
                                                   output_filename))
    print "Linking executable:", \
        host_os.path.relpath(output_filename, self.output_dir)
    self._link(objects, *list_args, **dict_args)

  def _link(self, objects, output_filename, output_dir=None, debug=False,
            extra_preargs=None, extra_postargs=None, target_lang=None):
    raise NotImplementedError

  def _setup_link(self, objects, output_dir, libraries, library_dirs):
    """Typecheck and fix up some of the arguments supplied to the class of link
    methods.  Specifically: ensure that all arguments are lists, and augment
    them with their permanent versions (eg. 'self.libraries' augments
    'libraries'). Return a tuple with fixed versions of all arguments.
    """
    if type (objects) not in (ListType, TupleType):
      raise TypeError("'objects' must be a list or tuple of strings")
    objects = list(objects)
    if output_dir is None:
      output_dir = self.output_dir
    elif type (output_dir) is not StringType:
      raise TypeError("'output_dir' must be a string or None")
    if libraries is None:
      libraries = self.libraries
    elif typecheck.is_sequence(libraries):
      libraries = list(libraries) + (self.libraries or [])
    else:
      raise TypeError("'libraries' (if supplied) must be a list of strings")
    if library_dirs is None:
      library_dirs = self.library_dirs
    elif type (library_dirs) in (ListType, TupleType):
      library_dirs = list (library_dirs) + (self.library_dirs or [])
    else:
      raise TypeError("'library_dirs' (if supplied) must be a list of strings")
    return objects, output_dir, libraries, library_dirs
