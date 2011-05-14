
import os

from builder.compilers.c import new_ccompiler
from builder.project import Extension, Project

#_______________________________________________________________________________

class CProject(Project):
    """C project for c-like compilers."""
    def __init__(self, name, sources=[], version=None, verbose=False, 
                 compiler=None, loader=None):
        Project.__init__(self, name, sources, version, verbose, compiler, 
                         loader)
        # Set the compiler if such was not defined
        if not self.compiler:
            self.compiler = new_ccompiler()

    def _build(self, sources, include_dirs=[], macros=[], 
               libraries=[], library_dirs=[], dry_run=False):
        self.output_filename = os.path.join(self.compiler.get_output_dir(), self.get_name())

        built_objects = self.compiler.compile(sources, 
                                              include_dirs=include_dirs,
                                              macros=macros)
        self.compiler.link(built_objects, self.output_filename, 
                           libraries=libraries,
                           library_dirs=library_dirs)

    def load(self):
        pass # pass it for simulation

