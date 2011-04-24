
class MetaData:
    def __init__(self, name=None, version=None):
        self.name = name or "UNKNOWN"
        self.version = version or "0.0.0"

    def get_name(self):
        return self.name

    def get_version(self):
        return self.version

# class MetaData

