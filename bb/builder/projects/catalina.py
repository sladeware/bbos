
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os.path

from bb.builder.compilers.catalina import CatalinaCompiler
from bb.builder.projects.c import CProject
from bb.builder.errors import *

#_______________________________________________________________________________

class CatalinaProject(CProject):
    """This type of project is working with Catalina compiler 
    (see builder.compilers.catalina.CatalinaCompiler)."""
    def __init__(self, *arglist, **argdict):
        CProject.__init__(self, compiler=CatalinaCompiler(), *arglist, **argdict)

    def _build(self, sources=None, output_dir=None, include_dirs=[], macros=[], 
               libraries=[], library_dirs=[]):
        """Start to build Catalina project."""
        CProject._build(self, sources, output_dir, include_dirs, macros, libraries, 
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
        
    def load(self, *arg_list, **arg_dict):
        self.loader.load(self.output_filename, *arg_list, **arg_dict)
