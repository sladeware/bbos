
from types import *

class Metadata:
    name = "UNKNOWN"

    def __init__(self, name=None, version=None):
        if name:
            self.set_name(name)
        self.version = version or "0.0.0"

    def set_name(self, name):
        if not type(name) is StringType:
            raise TypeError("Name must be string")
        self.name = name

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version



