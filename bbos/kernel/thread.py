
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

from bbos.component import Component

class Thread(Component):
    """
    Thread base class.
    """
    def __init__(self, name, entry, alias=None):
        Component.__init__(self, name)
        self.entry = entry
        if not alias:
            alias = entry
        self.alias = alias

    def set_alias(self, alias):
        pass

    def get_entry(self):
        """
        Get thread entry function.
        """
        return self.entry

    def get_alias(self):
        """
        Get alias of entry function.
        """
        return self.alias

