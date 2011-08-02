#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import platform
from types import *

from bb.utils.distribution import DistributionMetadata
from bb.builder.compiler import Compiler
from bb.builder.loader import Loader
from bb.builder.errors import *

class Extension(object):
    """Interface!"""
    def on_add(self, project):
        """This event will be called each time the extension will be added to 
        the project. Initially it's called from project.add_source() or
        project.add_extension()."""
        raise NotImplementedError

    def on_remove(self, project):
        """This event will be called each time the extension will be removed 
        from the project. Initially it's called from project.remove_source() 
        or project.remove_extension()."""
        raise NotImplementedError

    def on_build(self, project):
        """Called each time before the project is going to be built."""
        raise NotImplementedError

    def on_load(self, project):
        """Called each time before the project os going to be load."""
        raise NotImplementedError

#______________________________________________________________________________

_wrappers = {}

def get_wrapper(klass):
    if not klass.__name__ in _wrappers:
        return None
    return _wrappers[klass.__name__]

def wrap(obj):
    wrapper = get_wrapper(obj.__class__)
    if not wrapper:
        return None
    return wrapper(obj)

class Wrapper(Extension):
    """Interface!"""
    mapping = {}

    def __init__(self, target):
        Extension.__init__(self)
        for (event, action) in self.mapping.items():
            method = MethodType(action, target)
            setattr(self, event, method)

    @classmethod
    def bind(_, event, klass):
        def decorate(action):
            target_klass = klass
            if not isinstance(target_klass, Extension):
                target_klass = get_wrapper(klass)
                if not target_klass:
                    target_klass = type('_' + klass.__name__, (Wrapper,), dict(mapping={}))
                    _wrappers[klass.__name__] = target_klass
                target_klass.mapping[event] = action
            return action
        return decorate

#______________________________________________________________________________

class Project(DistributionMetadata):
    def __init__(self, name, sources=[], version=None, verbose=False, 
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
        """In the case when source is a path, it will be normalized by
        using os.path.abspath()."""
        if source:
            if type(source) is InstanceType:
                if isinstance(source, Extension):
                    return self.add_extension(source)
                wrapper = wrap(source)
                if not wrapper:
                    raise TypeError("Don't know how to work with %s object, "
                                    "the wrapper wasn't provided" % source)
                return self.add_extension(wrapper)
            elif type(source) is StringType:
                source = os.path.abspath(source)
                self.sources.append(source)
            else:
                raise TypeError("unknown source type: %s" % type(source))

    def add_sources(self, sources):
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

    # --- Compiler methods ---

    def set_compiler(self, compiler):
        if not isinstance(compiler, Compiler):
            raise UnknownCompiler
        self.compiler = compiler

    def get_compiler(self):
        return self.compiler

    # --- Loader methods ---

    def set_loader(self, loader):
        if not isinstance(loader, Loader):
            raise UnknownLoader
        self.loader = loader

    def has_extensions(self):
        return len(self.extensions)

    def build(self, sources=[], output_dir=None, verbose=None, 
              dry_run=None, 
              *arg_list, **arg_dict):
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        if self.verbose:
            print "Building project '%s' version '%s'" % (self.get_name(), self.get_version())
            self.compiler.verbose = self.verbose
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Dry run
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
        raise NotImplementedError



