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
import platform
import types

from bb import builder
from bb.builder import compilers
from bb.builder import loaders
from bb.builder import errors

class Project(object):
    """Class representing a project."""
    def __init__(self, name, sources=[], version=None,
                 verbose=False,
                 compiler=None, loader=None):
        self.__name = name
        self.__version = version
        self.verbose = verbose
        self.sources = []
        self.compiler = compiler
        self.loader = loader
        # A mapping object representing the string environment.
        self.env = {
            'HOST_OS': platform.system(), # XXX Hmmm.... so what about os.name?
            'HOST_PROCESSOR': platform.processor(),
            'HOST_ARCH': platform.machine(),
            }
        # ! The sources must be added at the end of initialization
        self.add_sources(sources)

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name or "UNKNOWN"

    def get_version(self):
        return self.__version or "0.0.0"

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
            self.sources.append(source)
        else:
            raise TypeError("unknown source type: %s" % type(source))

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

    def build(self, sources=[], output_dir=None,
              verbose=None,
              dry_run=None,
              *arg_list, **arg_dict):
        """Start building process."""
        # Control verbose
        if not verbose:
            verbose = builder.get_config().options.verbose
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        print "Building '%s'" % self.get_name()
        if self.verbose:
            self.compiler.verbose = self.verbose
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Control dry run mode
        if not dry_run:
            dry_run = builder.get_config().options.dry_run
        if dry_run is not None:
            self.compiler.dry_run = dry_run
        self.compiler.check_executables()
        # Run specific build process
        assert len(self.get_fixed_sources()), "Nothing to build"
        self._build(sources=self.get_fixed_sources(), *arg_list, **arg_dict)

    def _build(self, *arg_list, **arg_dict):
        raise NotImplementedError

    def load(self, *arg_list, **arg_dict):
        """Start loading the binary."""
        raise NotImplementedError
