
from bb.hardware import Device

class Core(Device):
    """Base class used to represent a core within a processor.

    A Core is the smallest computational unit supported by BBOS. There is one
    core per processes and one process per core."""
    def __init__(self, name, mapping=None):
        Device.__init__(self, name)
        __mapping = None
        __owner = None
        if mapping:
            self.set_mapping(mapping)

    def power_on(self):
        if not self.get_mapping():
            return

    def set_mapping(self, mapping):
        #if not isinstance(mapping, app.Mapping):
        #    raise TypeError('mapping must be %s sub-class'
        #                    % app.Mapping.__class__.__name__)
        self.__mapping = mapping
        mapping.hardware.set_core(self)

    def get_mapping(self):
        return self.__mapping
