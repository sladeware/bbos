#!/usr/bin/env python
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

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

import os
import os.path
import platform
import types
import inspect
import sys

from bb.builder import builder

from bb.builder.errors import *
from bb.utils.spawn import which, ExecutionError

class ProgramHandler(object):
    DEFAULT_EXECUTABLES = dict()
    """Default executables."""

    def __init__(self):
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
        """Check compiler executables. All of them has to exist. Print warning
        if some executable was specified but not defined.
        """
        if not self.__executables:
            return
        for (name, cmd) in self.__executables.items():
            if not cmd:
                print "WARNING: undefined executable '%s'" % name
                continue
            if not which(cmd[0]):
                raise ExecutionError("executable '%s' can not be found" % cmd[0])

class Compiler(ProgramHandler):
    """The basic compiler class."""

    def __init__(self, verbose=None, dry_run=False):
        self.verbose = verbose
        self.dry_run = dry_run
        # A common output directory for objects, libraries, etc.
        self.output_dir = ""
        self.output_filename = ""
        ProgramHandler.__init__(self)

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

class Toolchain(object):
    """This class represents a toolchain."""

    class Package(object):
        FILES = ()

        def __init__(self, toolchain, obj):
            self.__files = []
            if self.FILES:
                self.add_files(self.FILES)
            self.__object = obj
            self.__toolchain = toolchain

        def get_object(self):
            return self.__object

        def add_files(self, files):
            for file in files:
                self.add_file(file)

        def get_files(self):
            return self.__files

        def add_file(self, file):
            if not os.path.exists(file):
                package_file = inspect.getsourcefile(self.__class__)
                package_dirname = os.path.dirname(package_file)
                alternative_file = os.path.join(package_dirname, file)
                if not os.path.exists(alternative_file):
                    print "WARNING: file '%s' cannot be found" % file
                    return
                file = alternative_file
            self.__files.append(file)

        def get_toolchain(self):
            return self.__toolchain

        def on_unpack(self):
            """This event will be called each time the extension will be added
            to the project. Initially it's called from project.add_source() or
            project.add_extension().
            """
            files = self.get_files()
            self.get_toolchain().add_sources(files)

        def on_remove(self):
            """This event will be called each time the extension will be removed
            from the toolchain. Initially it's called from
            :func:`Toolchain.remove_source` or :func:`Toolchain.remove_package`.
            """
            raise NotImplementedError

        def on_build(self):
            """Called each time before the project is going to be built."""
            raise NotImplementedError

        def on_load(self):
            """Called each time before the project os going to be load."""
            raise NotImplementedError

    storage = dict()

    def __init__(self, sources=[], version=None, verbose=False, compiler=None,
                 loader=None):
        self.verbose = verbose
        self.sources = []
        self.__packages = list()
        self.compiler = compiler
        self.loader = loader
        # A mapping object representing the string environment.
        self.env = {
            'HOST_OS': platform.system(), # XXX Hmmm.... so what about os.name?
            'HOST_PROCESSOR': platform.processor(),
            'HOST_ARCH': platform.machine(),
            }
        # NOTE: the sources must be added at the end of initialization
        self.add_sources(sources)

    @classmethod
    def pack(this_class, object_class, package_class=None):
        """Packing means creating package for an object. Can be also
        used as decorator.
        """
        def store(key, value):
            if not Toolchain.storage.get(this_class, None):
                Toolchain.storage[this_class] = dict()
            Toolchain.storage[this_class][key] = value
        if package_class:
            store(object_class, package_class)
            return
        # As decorator
        def catcher(package_class):
            store(object_class, package_class)
            return package_class
        return catcher

    @classmethod
    def get_package_class(toolchain_class, object_instance_or_class):
        object_class = None
        if type(object_instance_or_class) == types.TypeType:
            object_class = object_instance_or_class
        else:
            object_class = object_instance_or_class.__class__
        if not Toolchain.storage.get(toolchain_class, None):
            return None
        return Toolchain.storage[toolchain_class].get(object_class, None)

    def add_source(self, source):
        """Add a source to the project. In the case when source is a
        path, it will be normalized by using :func:`os.path.abspath`.
        """
        if not source:
            return
        if type(source) is types.StringType:
            source = os.path.abspath(source)
            if not os.path.exists(source):
                raise Exception("Source doesn't exist: %s" % source)
            print "Adding source '%s'" % source
            self.sources.append(source)
            return
        elif isinstance(source, object):
            package = self.__get_package_by_object(source)
            if package:
                self.unpack_package(package)
                return
        print "WARNING: unknown source type '%s' of '%s'" % (type(source), source)

    def __get_package_by_object(self, obj):
        package_class = self.get_package_class(obj)
        if not package_class:
            #raise TypeError('cannot define package for the source %s' % source)
            return None
        package = package_class(self, obj)
        return package

    def unpack_package(self, package):
        self.__packages.append(package)
        print "Unpacking package '%s'..." % (package.__class__.__name__,)
        try:
            package.on_unpack()
        except NotImplementedError:
            pass

    def add_sources(self, sources):
        """Add and process a list sources at once."""
        if not type(sources) == types.ListType:
            raise TypeError
        for source in sources:
            self.add_source(source)

    def get_sources(self):
        return self.sources

    def get_fixed_sources(self):
        sources = []
        for source in self.get_sources():
            sources.append(os.path.abspath(source))
        return sources

    def set_compiler(self, compiler):
        """Set and return compiler instance that will be used in
        compilation process. The `compiler` has to be a sub-class of
        :class:`bb.builder.compilers.compiler.Compiler`.
        """
        if not isinstance(compiler, compilers.Compiler):
            raise errors.UnknownCompiler
        self.compiler = compiler
        return compiler

    def get_compiler(self):
        """Return the :class:`bb.builder.compilers.compiler.Compiler`
        compiler instance.
        """
        return self.compiler

    def set_loader(self, loader):
        """Set loader instance that will help us to load the binary on
        hardware. The `loader` has to be a sub-class of
        :class:`bb.builder.loaders.loader.Loader`.
        """
        if not isinstance(loader, loaders.Loader):
            raise errors.UnknownLoader
        self.loader = loader

    def build(self, sources=[], output_dir=None, verbose=None, dry_run=None,
              *arg_list, **arg_dict):
        """Start building process."""
        # Control verbose
        if not verbose:
            verbose = builder.get_config().options.verbose
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Control dry run mode
        if not dry_run:
            dry_run = builder.get_config().options.dry_run
        print 'Building...'
        if self.compiler:
            self.compiler.check_executables()
            if dry_run is not None:
                self.compiler.dry_run = dry_run
            if self.verbose:
                self.compiler.verbose = self.verbose
        # Run specific build process
        if not len(self.get_fixed_sources()):
            print "Nothing to build"
            return
        self._build(sources=self.get_fixed_sources(), *arg_list, **arg_dict)

    def _build(self, *arg_list, **arg_dict):
        raise NotImplementedError

    def load(self, *arg_list, **arg_dict):
        """Start loading the binary."""
        raise NotImplementedError
