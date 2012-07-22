#!/usr/bin/env python

import imp
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG)

_import_build = False
_builds = list()

def do_import_build():
    global _import_build, _builds
    _import_build = True
    if not len(_builds):
        return
    for build in _builds:
        BBImporter.load_package(build)

class BBImporter(object):
    """Read more about import hooks here
    <http://www.python.org/dev/peps/pep-0302/>,
    <http://docs.python.org/py3k/library/importlib.html>,
    <http://docs.python.org/library/imp.html>."""

    def find_module(self, fullname, path=None):
        # Control only bb. modules
        if fullname == 'bb' or fullname.startswith('bb.'):
            return self
        return None

    @classmethod
    def load_package(klass, fullname):
        setup = fullname + "_build"
        search_path, mod_path = klass.get_filename(setup)
        if not search_path and not mod_path:
            return
        file_path = os.path.join(search_path, mod_path + ".py")
        klass.load_source(setup, file_path)

    @classmethod
    def load_source(klass, fullname, file_path):
        logging.debug("Load '%s'", file_path)
        imp.load_source(fullname, file_path)

    def load_buildtime_module(self, fullname):
        fullname = "bb" + fullname[12:]
        if fullname in sys.modules:
            return sys.modules[fullname]
        raise ImportError("module cannot be found")

    @classmethod
    def get_filename(klass, fullname, path=None):
        fullname = fullname.split(".")
        filename = None
        files = []
        for search_path in sys.path:
            path = search_path
            parts = ""
            for part in fullname:
                parts = os.path.join(parts, part)
                path = os.path.join(search_path, parts)
                if os.path.exists(path) and os.path.isdir(path):
                    files.append((search_path, os.path.join(parts, "__init__")))
                    continue
                if os.path.exists(path + ".py"):
                    files.append((search_path, parts))
                    continue
                files = []
                break
            if files:
                break
        if files:
            return files.pop()
        return (None, None)

    def is_package(self, fullname):
        """Looks for an __init__ file name as returned by get_filename()."""
        search_path, mod_path = self.get_filename(fullname)
        filename = os.path.basename(mod_path)
        return filename == '__init__'

    def get_mod_path(self, fullname):
        search_path, mod_path = self.get_filename(fullname)
        if mod_path and mod_path.endswith('__init__'):
            mod_path = mod_path[:len(mod_path) - 9]
        return mod_path

    def load_module(self, fullname):
        global _import_build, _builds
        if fullname in sys.modules:
            if _import_build:
                self.load_package(fullname)
            return sys.modules[fullname]
        mod = None
        if fullname.startswith('bb.buildtime'):
            mod = self.load_buildtime_module(fullname)
        else:
            mod_path = self.get_mod_path(fullname)
            if not mod_path:
                return None
            fh, path, descr = imp.find_module(mod_path)
            sys.modules.setdefault(fullname, imp.new_module(fullname))
            mod = imp.load_module(fullname, fh, path, descr)
        mod.__loader__ = self
        mod.__file__ = "<%s>" % self.__class__.__name__
        if self.is_package(fullname):
            mod.__path__ = ""
            mod.__package__ = fullname
        else:
            mod.__package__ = fullname.rpartition('.')[0]
        if _import_build:
            self.load_package(fullname)
        else:
            _builds.append(fullname)
        return mod

sys.meta_path = [BBImporter()]
