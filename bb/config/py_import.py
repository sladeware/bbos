#!/usr/bin/env python

import imp
import sys

class BBImport(object):
    """Read more about import hooks here
    <http://www.python.org/dev/peps/pep-0302/>."""

    # TODO: add 'bb.runtime' later
    magic_namespaces = ('bb.buildtime',)

    def find_module(self, fullname, path=None):
        for magic_namespace in self.magic_namespaces:
            if fullname.startswith(magic_namespace):
                return self
        return None

    def load_runtime_module(self, fullname):
        pass

    def load_buildtime_module(self, fullname):
        fullname = "bb" + fullname[12:]
        if fullname in sys.modules:
            return sys.modules[fullname]
        raise ImportError("module cannot be found")

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = None
        if fullname.startswith('bb.runtime'):
            # TODO: pass for now in case of modules bb.runtime and bb.buildtime
            # we will create a fake modules
            #
            # mod = self.load_runtime_module(fullname)
            print ">>>>", fullname
        elif fullname.startswith('bb.buildtime'):
            mod = self.load_buildtime_module(fullname)
        else:
            return mod
        mod.__loader__ = self
        sys.modules[fullname] = mod
        mod.__file__ = "[mirror]"
        mod.__path__ = []
        return mod

sys.meta_path = [BBImport()]
