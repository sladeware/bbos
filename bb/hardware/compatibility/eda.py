
import os.path

class EDA(object):
    # User defined fritzing home directory that can be set with help of
    # X.set_home_dir() function.
    home_dir = None

    @classmethod
    def get_home_dir(cls):
        """Return path to the directory with fritzing distribution."""
        return cls.home_dir

    @classmethod
    def set_home_dir(cls, path):
        if not os.path.exists(path):
            raise IOError("Directory '%s' does not exist" % path)
        cls.home_dir = path

