
from builder.compilers.c import new_ccompiler
from builder.project import Extension, Project

#_______________________________________________________________________________

class CProject(Project):
    """C project for c-like compilers."""
    def __init__(self, name, sources=[], version=None, verbose=False, 
                 dry_run=False):
        Project.__init__(self, name, sources, version, verbose, dry_run)
        # Set the compiler
        self.compiler = new_ccompiler(verbose=self.verbose, 
                                      dry_run=self.dry_run)

    def _build(self, sources=None, include_dirs=[], macros=[], libraries=[], 
               library_dirs=[]):

        assert len(self.sources), "Nothing to build"

        self.output_filename = self.get_name()

        built_objects = self.compiler.compile(self.sources, 
                                        include_dirs=include_dirs,
                                        macros=macros)
        self.compiler.link(built_objects, self.output_filename, 
                           libraries=libraries,
                           library_dirs=library_dirs)

    def load(self):
        pass # pass it for simulation

