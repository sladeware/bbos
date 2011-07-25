
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component

#_______________________________________________________________________________

class Thread(Component):
    """Thread base class."""
    def __init__(self, name, entry, alias=None):
        Component.__init__(self, name)
        self.entry = entry
        if not alias:
            alias = entry
        self.set_alias(alias)
    # __init__()

    def set_alias(self, alias):
        self.alias = alias
    # set_alias()

    def get_entry(self):
        """Get thread entry function."""
        return self.entry
    # get_entry()

    def get_alias(self):
        """Get alias of entry function."""
        return self.alias
    # get_alias()

