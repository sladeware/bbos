#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import platform
from types import *

import bb.builder
from bb.utils.distribution import DistributionMetadata
from bb.builder.compilers import Compiler
from bb.builder.loaders import Loader
from bb.builder.errors import *

class Project(DistributionMetadata):
    """Class representing a project."""
    def __init__(self, name, sources=[], version=None,
                 verbose=False,
                 compiler=None, loader=None):
        DistributionMetadata.__init__(self, name, version)
        self.verbose = verbose
        self.sources = []
        self.extensions = []
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

    def add_extension(self, ext):
        self.extensions.append(ext)
        try:
            ext.on_add(self)
        except NotImplementedError:
            pass

    def add_source(self, source):
        """Add a source to the project. In the case when source is a
        path, it will be normalized by using :func:`os.path.abspath`."""
        if not source:
            return
        if type(source) is StringType:
            source = os.path.abspath(source)
            if not os.path.exists(source):
                raise Exception("Source doesn't exist: %s" % source)
            self.sources.append(source)
        elif type(source) is InstanceType or isinstance(source, object):
            if isinstance(source, Extension):
                return self.add_extension(source)
            wrapper = wrap(source)
            if not wrapper:
                raise TypeError("Don't know how to work with '%s' object. "
                                "The wrapper wasn't provided." % source)
            return self.add_extension(wrapper)
        else:
            raise TypeError("unknown source type: %s" % type(source))

    def add_sources(self, sources):
        """Add and process a list sources at once."""
        if not type(sources) == ListType:
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
        """Set compiler instance that will be used in compilation
        process. The `compiler` has to be a sub-class of
        :class:`bb.builder.compilers.compiler.Compiler`."""
        if not isinstance(compiler, Compiler):
            raise UnknownCompiler
        self.compiler = compiler

    def get_compiler(self):
        """Return the :class:`bb.builder.compilers.compiler.Compiler`
        compiler instance."""
        return self.compiler

    def set_loader(self, loader):
        """Set loader instance that will help us to load the binary on
        hardware. The `loader` has to be a sub-class of
        :class:`bb.builder.loaders.loader.Loader`."""
        if not isinstance(loader, Loader):
            raise UnknownLoader
        self.loader = loader

    def has_extensions(self):
        return len(self.extensions)

    def build(self, sources=[], output_dir=None,
              verbose=None,
              dry_run=None,
              *arg_list, **arg_dict):
        """Start building process."""
        # Control verbose
        if not verbose:
            verbose = getattr(bb.builder.config.options, 'verbose', verbose)
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        print "Building project '%s' version '%s'" % (self.get_name(), self.get_version())
        if self.verbose:
            self.compiler.verbose = self.verbose
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Control dry run mode
        if not dry_run:
            dry_run = getattr(bb.builder.config.options, 'dry_run', dry_run)
        if dry_run is not None:
            self.compiler.dry_run = dry_run
        self.compiler.check_executables()
        # Prepare extensions
        if self.has_extensions():
            for extension in self.extensions:
                try:
                    extension.on_build(self)
                except NotImplementedError:
                    pass
        # Run specific build process
        assert len(self.get_fixed_sources()), "Nothing to build"
        self._build(sources=self.get_fixed_sources(), *arg_list, **arg_dict)

    def _build(self, *arg_list, **arg_dict):
        raise NotImplementedError

    def load(self, *arg_list, **arg_dict):
        """Start loading the binary."""
        raise NotImplementedError
