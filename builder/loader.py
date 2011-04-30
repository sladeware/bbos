
from types import *

from builder.errors import *

#_______________________________________________________________________________

class Loader(object):
    """Abstract base class to define the interface that must be implemented by
    real loader classes."""

    executables = {}

    def __init__(self, verbose=False):
        self.verbose = verbose
    # __init__()

    def load(self, *arg_list, **arg_dict):
        print "Loading"
        self._load(*arg_list, **arg_dict)

    def _load(self, *arg_list, **arg_dict):
        raise NotImplemented
    # load()

