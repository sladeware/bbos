
import os.path

from builder.compilers.catalina import CatalinaCompiler
from builder.projects.c import CProject
from builder.errors import *

#_______________________________________________________________________________

class CatalinaProject(CProject):
    """This type of project is working with Catalina compiler 
    (see builder.compilers.catalina.CatalinaCompiler)."""
    def __init__(self, *arglist, **argdict):
        CProject.__init__(self, *arglist, **argdict)
        self.compiler = CatalinaCompiler(self.verbose, self.dry_run)
    # __init__()

    def _build(self, sources=None, include_dirs=[], macros=[], libraries=[], 
               library_dirs=[]):
        """Start to build Catalina project."""
        CProject._build(self, sources, include_dirs, macros, libraries, 
               library_dirs)

        # Catalina will add to the output_path file .binary extension in case 
        # of binary output (see -b option) and .eeprom extension is case of
        # eeprom output (see -e option). That's why it additionaly should be 
        # handled after the compilation and linking.
        self.output_filename = "%s.binary" % self.output_filename

        # We have to be sure that output_path file has been produced, otherwise
        # it want be load
        if not os.path.exists(self.output_filename):
            raise BuilderError, "It seems like output file '%s' has not been " \
                "produced" % self.output_filename
    # _build()
        
    def load(self):
        self.loader.load(self.output_filename)
    # load()
