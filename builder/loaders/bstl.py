
from builder.errors import *
from builder.loader import Loader
from builder.spawn import spawn

#_______________________________________________________________________________

class BSTLLoader(Loader):
    """BSTL is the command line loader which can be found here
    http://www.fnarfbargle.com/bst.html

    This little application simply allows to load pre-compiled .binary 
    and .eeprom files into your propeller. It is a command line 
    application that takes optional parameters and a file name."""

    executables = {
        'loader' : ['bstl']
        }

    def __init__(self, verbose=False):
        Loader.__init__(self, verbose)
        self.device = None
        self.mode = 1
        
    def _load(self, filename, device=None, mode=1):
        loader = self.executables['loader']
        try:
            spawn(loader + [filename],
                  verbose=self.verbose)
        except BuilderExecutionError, msg:
            raise LoaderError, msg


