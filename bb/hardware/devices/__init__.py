#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Alexander Sviridenko"

from bb.hardware.devices.device import *

# XXX: The following code is temporary frozen.
def find_pkg_files(pkg, root=None, skip_names=[], recursive=True):
    verify_list(skip_names)
    verify_string(pkg)
    if not root:
        pkgs = pkg.split(".")
        pkg_half_path = os.path.sep.join(pkgs)
        root = None
        for path in sys.path:
            path = os.path.join(path, pkg_half_path)
            if os.path.exists(path):
                root = path
                break
    files = list()
    for name in os.listdir(root):
        if name in skip_names:
            continue
        path = os.path.join(root, name)
        if os.path.isdir(path) and recursive:
            if name.startswith("."): # improve this
                continue
            files.extend(find_pkg_files(".".join([pkg, name]), path, skip_names))
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(".".join([pkg, name])) #(os.path.abspath(path))
    return files

def index_parts():
    skip_names = ["__init__.py"]
    for module_name in find_pkg_files("bb.hardware.parts", None, skip_names):
        module = __import__(module_name, globals())
        names = getattr(module, "__parts__", None)
        if not names:
            continue
        #for name in names:
        #    part_class = getattr(module, name, None)

#index_parts()
