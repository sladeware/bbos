#!/usr/bin/env python

import os.path
import platform

from bb.lib.utils import typecheck

class Toolchain(object):
    def __init__(self, sources=[], verbose=False, compiler=None, loader=None):
        if not typecheck.is_list(sources):
            raise Exception("Must be list")
        self._verbose = verbose
        self._sources = []
        self._compiler = None
        self._loader = None
        self._env = {
            'HOST_OS': platform.system(), # NOTE: what about os.name?
            'HOST_PROCESSOR': platform.processor(),
            'HOST_ARCH': platform.machine(),
            }
        if compiler:
            self.set_compiler(compiler)
        if loader:
            self.set_loader(loader)
        # NOTE: the sources must be added at the end of initialization
        if sources:
            self.add_sources(sources)

    def add_sources(self, sources):
        if not typecheck.is_list(sources):
            raise TypeError()
        for source in sources:
            self.add_source(source)

    def get_sources(self):
        return self._sources

    def add_source(self, source):
        """Add a source to the project. In the case when source is a
        path, it will be normalized by using :func:`os.path.abspath`.
        """
        if not source:
            raise Exception("WTF!")
        if typecheck.is_string(source):
            source = os.path.abspath(source)
            if not os.path.exists(source):
                raise Exception("Source doesn't exist: %s" % source)
            print "Adding source '%s'" % source
            self._sources.append(source)
            return
        raise TypeError("unknown source type '%s' of '%s'"
                        % (type(source), source))

    def get_compiler(self):
        return self._compiler

    @property
    def compiler(self):
        return self.get_compiler()

    def get_loader(self):
        return self._loader

    @property
    def loader(self):
        return self.get_loader()

    def build(self, sources=[], output_dir=None, verbose=None, dry_run=None,
              *arg_list, **arg_dict):
        """Start building process."""
        # Control verbose
        if not verbose:
            verbose = 1
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Control dry run mode
        if not dry_run:
            dry_run = 0
        print 'Building...'
        if self.compiler:
            self.compiler.check_executables()
            if dry_run is not None:
                self.compiler.dry_run = dry_run
            if self.verbose:
                self.compiler.verbose = self.verbose
        # Run specific build process
        if not len(self.get_sources()):
            print "Nothing to build"
            return
        self._build(*arg_list, **arg_dict)

    def _build(self, *arg_list, **arg_dict):
        raise NotImplementedError
