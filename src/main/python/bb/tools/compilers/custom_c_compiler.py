# http://www.bionicbunny.org/
# Copyright (c) 2012-2013 Sladeware LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Oleksandr Sviridenko

# TODO: Move linker specific API from Compiler class to Linker class and start
# using it.

import os
import os.path
import sys
import time

import bb.config
from bb.tools.compilers.compiler import Compiler
from bb.utils import path_utils
from bb.utils import typecheck
from bb.utils import logging
from bb.utils import executable

logger = logging.get_logger("bb")

class Linker(object):
  """Base linker class."""

  def __init__(self):
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

  def link(self, objects, output_filename, *list_args, **dict_args):
    # Adopt output file name to output directory
    if self.get_output_dir() is not None:
      self.set_output_filename(path_utils.join(self.get_output_dir(),
                                                 output_filename))
    binary_filename = path_utils.relpath(output_filename, self.output_dir)
    logger.info("Linking executable: %s" % binary_filename)
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
  :func:`CustomCCompiler.set_language_precedence_order`. By default it equals to
  :const:`CustomCCompiler.LANGUAGE_PRECEDENCE_ORDER`.

  Learn more about GCC options:
  http://gcc.gnu.org/onlinedocs/gcc/Option-Summary.html
  """

  default_output_filename = "a.out"
  source_extensions = None
  object_extension = None

  def __init__(self, verbose=0, dry_run=False):
    Compiler.__init__(self, verbose, dry_run)
    self._output_dir = None
    self._output_file = None
    # A list of macro definitions (we are using list since the order is
    # important). A macro definition is a 2-tuple (name, value), where the value
    # is either a string or None. A macro undefinition is a 1-tuple (name,).
    self.macros = list()
    # A list of directories
    self._include_dirs = list()
    # A list of library names (not filenames: eg. "foo" not "libfoo.a")
    # to include in any link
    self.libraries = list()
    # A list of directories to seach for libraries
    self.library_dirs = list()
    # A list of object files
    self.objects = list()
    self._object_extension = None
    self.set_object_extension(self.object_extension)
    self._source_extensions = list()
    self.set_source_extensions(self.source_extensions)
    self._extra_preopts = list()
    self._extra_postopts = list()
    self._linker = None

  def set_output_dir(self, path):
    if not typecheck.is_string(path):
      raise TypeError("'path' must be a string")
    self._output_dir = path

  def get_output_dir(self):
    """Returns path to output directory.

    .. todo:: Always returns path to b3 build directory. Fix this.

    :returns: A string that represents directory path.
    """
    if self._output_dir:
      return self._output_dir
    return bb.config.user_settings.get("b3", "builddir")

  def get_default_ccompiler(osname=None, platform=None):
    """Determine the default compiler to use for the given `platform`.

    `osname` should be one of the standard Python OS names (i.e. the ones
    returned by os.name) and platform the common value returned by
    ``sys.platform`` for the platform in question.

    The default values are os.name and ``sys.platform`` in case the
    parameters are not given.
    """
    if osname is None:
      osname = os.name
    if platform is None:
      platform = sys.platform
    for pattern, compiler in CCOMPILERS:
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

  def get_object_extension(self):
    """Return object file extension."""
    return self._object_extension

  def set_object_extension(self, extension):
    """The `extension` argument is case-insensitive and can be
    specified with or without a leading dot.
    """
    self._object_extension = extension

  def _find_macro(self, name):
    """Return position of the macro 'name' in the list of macros."""
    i = 0
    for macro in self.macros:
      if macro[0] == name:
        return i
      i += 1
    return None

  def add_include_dirs(self, pathes):
    """Add a list of dirs `pathes` to the list of directories that will be
    searched for header files. See :func:`add_include_dir`.

    :param pathes: A list of strings.

    :raises: TypeError
    """
    if not typecheck.is_list(pathes):
      raise TypeError()
    for path in pathes:
      self.add_include_dir(path)

  def add_include_dir(self, path):
    """Add `path` to the list of directories that will be searched for header
    files. The compiler is instructed to search directories in the order in
    which they are supplied by successive calls to :func:`add_include_dir()`.
    """
    if not typecheck.is_string(path):
      raise TypeError()
    self._include_dirs.append(path)

  def get_include_dirs(self):
    return self._include_dirs

  def add_library(self, library_name):
    """Add `library_name` to the list of libraries that will be included in all
    links driven by this compiler object. Note that `library_name` should *not*
    be the name of a file containing a library, but the name of the library
    itself: the actual filename will be inferred by the linker, the compiler, or
    the compiler class (depending on the platform).

    The linker will be instructed to link against libraries in the order they
    were supplied to :func:`add_library` and/or :func:`set_libraries`. It is
    perfectly valid to duplicate library names; the linker will be instructed to
    link against libraries as many times as they are mentioned.
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
    libraries in the order they are supplied to :func:`add_library_dir` and/or
    :func:`set_library_dirs`.
    """
    self.library_dirs.append(library_dir)

  def add_library_dirs(self, dirs):
    if dirs and typecheck.is_sequence(dirc):
      for library_dir in list(dirs):
        self.add_library_dir(library_dir)
    else:
      raise TypeError("'dirs' (if supplied) must be a list of strings")

  def add_link_object(self, obj):
    """Add `obj` to the list of object files (or analogues, such as explicitly
    named library files or the output of "resource compilers") to be included in
    every link driven by this compiler object.
    """
    self.objects.append(obj)

  def add_link_objects(self, objects):
    """See :func:`CCompiler.add_link_object`."""
    if typecheck.is_sequence(objects):
      raise TypeError("'objects' must be a list or tuple of strings")
    for obj in list(objects):
      self.add_link_object(obj)

  def define_macro(self, name, value=None):
    """Define a preprocessor macro for all compilations driven by this compiler
    object. The optional parameter `value` should be a string; if it is not
    supplied, then the macro will be defined without an explicit value and the
    exact outcome depends on the compiler used (XXX true? does ANSI say anything
    about this?)
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
    language_map, and :func:`CCompiler.get_language_precedence_order` to do the
    job.
    """
    if not typecheck.is_list(sources):
      sources = [sources]
    lang = None
    index = len(self.language_order)
    for source in sources:
      base, ext = path_utils.splitext(source)
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
    """Return the compiler option to add 'dir' to the list of directories
    searched for libraries.
    """
    raise NotImplemented

  def get_library_option(self, lib):
    """Return the compiler option to add 'dir' to the list of libraries linked
    into the shared library or executable.
    """
    raise NotImplementedError

  def find_library_file (self, dirs, lib, debug=0):
    """Search the specified list of directories for a static or shared library
    file `lib` and return the full path to that file. If `debug` true, look for
    a debugging version (if that makes sense on the current platform). Return
    ``None`` if `lib` wasn't found in any of the specified directories.
    """
    raise NotImplementedError

  def _gen_lib_options(self, library_dirs, libraries):
    """Generate linker options for searching library directories and linking
    with specific libraries. 'libraries' and 'library_dirs' are, respectively,
    lists of library names (not filenames!) and search directories. Returns a
    list of command-line options suitable for use with some compiler (depending
    on the two format strings passed in).
    """
    lib_options = []
    for dir in library_dirs:
      lib_options.append(self.get_library_dir_option(dir))
    # XXX it's important that we *not* remove redundant library mentions!
    # sometimes you really do have to say "-lfoo -lbar -lfoo" in order to
    # resolve all symbols.  I just hope we never have to say "-lfoo obj.o -lbar"
    # to get things to work -- that's certainly a possibility, but a pretty
    # nasty way to arrange your C code.
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
    """Macros is the usual thing, a list of 1- or 2-tuples, where (name,) means
    undefine (-U) macro 'name', and (name, value) means define (-D) macro 'name'
    to 'value'.
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
    """include_dirs is just a list of directory names to be added to the header
    file search path (-I).
    """
    options = []
    for include_dir in include_dirs:
      if not include_dir:
        continue
      options.append ("-I%s" % include_dir)
    return options

  def _gen_preprocess_options(self, macros, include_dirs):
    """Generate C pre-processor options(-D, -U, -I) as used by at least two
    types of compilers: the typical Unix compiler and Visual C++. Returns a list
    of command-line options suitable for either Unix compilers and Visual C++.
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

  def get_object_filenames(self, src_filenames):
    obj_filenames = []
    for src_filename in src_filenames:
      base, ext = path_utils.splitext(src_filename)
      base = path_utils.splitdrive(base)[1]
      base = base[path_utils.isabs(base):]
      if ext not in self.get_source_extensions():
        raise Exception("unknown file type '%s' of '%s'" % (ext, src_filename))
      obj_filenames.append(
        path_utils.join(self.get_output_dir(),
                             base + self.get_object_extension()))
    return obj_filenames

  def set_extra_preopts(self, extra_preopts):
    self._extra_preopts = extra_preopts

  def get_extra_preopts(self):
    return self._extra_preopts

  def set_extra_postopts(self, extra_postopts):
    self._extra_postopts = extra_postopts

  def get_extra_postopts(self):
    return self._extra_postopts

  def compile(self, files=[], output_file=None, macros=None,
              include_dirs=[], debug=False, extra_preopts=None,
              extra_postopts=[], depends=None, link=True):
    if not typecheck.is_list(files):
      raise TypeError("'sources' must be a list")
    files = files + self.get_files()
    # Play with extra preopts and postopts
    extra_preopts = self.get_extra_preopts()
    extra_postopts = self.get_extra_postopts()
    # Setup compilation process first
    if output_file:
      self.set_output_file(output_file)
    include_dirs = set(include_dirs).update(set(self.get_include_dirs()))
    macros, objects, extra_postopts, pp_options, build = \
        self._setup_compile(files, macros, include_dirs, extra_postopts, depends)
    cc_options = self._gen_cc_options(pp_options, debug, extra_preopts)
    for obj in objects:
      try:
        src, ext = build[obj]
      except KeyError:
        continue
      logger.info("Compiling %s" % src)
      # Note: we pass a copy of files, options, etc. since we
      # need to privent their modification
      if not self.is_dry_run_mode_enabled():
        self._compile(obj, src, ext, list(cc_options), extra_postopts, pp_options)
    if link is True:
      self.link(objects, self.get_output_filename())
    return objects

  def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
    """Compile source to product objects."""
    raise NotImplemented

  def _setup_compile(self, sources, macros, include_dirs, extra, depends):
    """Process arguments and decide which source files to compile."""
    if macros is None:
      macros = self.macros
    elif typecheck.is_list(macros):
      macros = macros + (self.macros or [])
    else:
      raise TypeError("'macros' (if supplied) must be a list of tuples")
    if include_dirs is None:
      include_dirs = self._include_dirs
    elif typecheck.is_sequence(include_dirs):
      include_dirs = list(include_dirs) + (self._include_dirs or [])
    else:
      raise TypeError("'include_dirs' (if supplied) must be a list of strings")
    if extra is None:
      extra = []
    # List of expected output files
    objects = self.get_object_filenames(sources)
    assert len(objects) == len(sources)
    pp_options = self._gen_preprocess_options(macros, include_dirs)
    build = {}
    for i in range(len(sources)):
      src = sources[i]
      obj = objects[i]
      ext = path_utils.splitext(src)[1]
      path_utils.mkpath(path_utils.dirname(obj), 0777)
      build[obj] = (src, ext)
    return macros, objects, extra, pp_options, build

  def link(self, objects, output_filename, *list_args, **dict_args):
    """Start linking process."""
    # Adopt output file name to output directory
    if not output_filename:
      raise Exception("output_filename must be provided")
    binary_filename = output_filename
    logger.info("Linking executable '%s'" % binary_filename)
    self._link(objects, *list_args, **dict_args)
    logger.info("Binary %s, %d byte(s)" % (binary_filename,
                                     os.path.getsize(binary_filename)))

  def _link(self, objects, output_file_name, output_dir=None, debug=False,
            extra_preargs=None, extra_postargs=None, target_lang=None):
    raise NotImplementedError

  def _setup_link(self, objects, output_dir, libraries, library_dirs):
    """Typecheck and fix up some of the arguments supplied to the class of link
    methods. Specifically: ensure that all arguments are lists, and augment them
    with their permanent versions (eg. 'self.libraries' augments
    'libraries'). Returns a tuple with fixed versions of all arguments.
    """
    if not typecheck.is_sequence(objects):
      raise TypeError("'objects' must be a list or tuple of strings")
    objects = list(objects)
    if output_dir is None:
      output_dir = self.get_output_dir()
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
    elif typecheck.is_sequence(library_dirs):
      library_dirs = list(library_dirs) + (self.library_dirs or [])
    else:
      raise TypeError("'library_dirs' (if supplied) must be a list of strings")
    return objects, output_dir, libraries, library_dirs
