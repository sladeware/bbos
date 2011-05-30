
import os
import platform
from types import *

from builder.compiler import Compiler
from builder.loader import Loader
from builder.metadata import Metadata
from builder.errors import *

#______________________________________________________________________________

class Extension(Metadata):
    def __init__(self, name=None, version=None):
        Metadata.__init__(self, name, version)

    def on_add(self, project):
        """This event will be called each time the extension will be added to 
        the project. Initially it's called from project.add_source() or
        project.add_extension()."""
        pass

    def on_remove(self, project):
        """This event will be called each time the extension will be removed 
        from the project. Initially it's called from project.remove_source() 
        or project.remove_extension()."""
        pass

    def on_build(self, project):
        """Called each time before the project is going to be built."""
        pass

    def on_load(self, project):
        """Called each time before the project os going to be load."""
        pass

    def attach(self, project):
        """A concrete extension class can either override this method
        entirely or implement _attach(), which is more secure."""
        if not isinstance(project, Project):
            raise Exception
        self._attach(project)

    def _attach(self, project):
        raise NotImplemented

    def detach(self, project):
        """A concrete extension class can either override this method
        entirely or implment _detach(), which is more secure."""
        if not isinstance(project, Project):
            raise Exception
        self._detach(project)

    def _detach(self, project):
        raise NotImplemented

#______________________________________________________________________________

class Project(Metadata):
    def __init__(self, name, sources=[], version=None, verbose=False, 
                 compiler=None, loader=None):
        Metadata.__init__(self, name, version)
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
        ext.on_add(self)

    def add_source(self, source):
        """In the case when source is a path, it will be normalized by
        using os.path.abspath()."""
        if source:
            if isinstance(source, Extension):
                return self.add_extension(source)
            source = os.path.abspath(source)
            self.sources.append(source)

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

    def set_compiler(self, compiler):
        if not isinstance(compiler, Compiler):
            raise UnknownCompiler
        self.compiler = compiler

    def set_loader(self, loader):
        if not isinstance(loader, Loader):
            raise UnknownLoader
        self.loader = loader

    def has_extensions(self):
        return len(self.extensions)

    def build(self, sources=[], output_dir=None, verbose=None, dry_run=None, 
              *arg_list, **arg_dict):
        if verbose is not None:
            self.verbose = verbose
        if sources:
            self.add_sources(sources)
        if self.verbose:
            print "Building project '%s' version '%s'" % (self.name, self.version)
        if output_dir:
            self.compiler.set_output_dir(output_dir)
        # Dry run
        if dry_run is not None:
            self.compiler.dry_run = dry_run
        # Prepare extensions
        if self.has_extensions():
            for extension in self.extensions:
                extension.on_build(self)
        # Run specific build process
        assert len(self.get_fixed_sources()), "Nothing to build"
        self._build(sources=self.get_fixed_sources(), *arg_list, **arg_dict)
        
    def _build(self, *arg_list, **arg_dict):
        raise NotImplemented

    def load(self, *arg_list, **arg_dict):
        raise NotImplemented



