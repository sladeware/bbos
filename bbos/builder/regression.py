"""BBOS Builder Regression testing framework
"""

__copyright__  = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

import os
import re
import sys
import unittest

def get_module_names(path):
    module_names = []
    files = os.listdir(path)
    test = re.compile("test\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    filename_to_module_name = lambda f: os.path.splitext(f)[0]
    module_names = map(filename_to_module_name, files)
    return module_names

def recursive_directory_walk(path):
    sys.path.append(path)
    basedir = path
    subdirlist = []
    module_names = []
    for item in os.listdir(path):
        my_dir = os.path.join(basedir, item)
        if os.path.isdir(my_dir):
            module_names += get_module_names(my_dir)
            subdirlist.append(my_dir)
    for subdir in subdirlist:
        module_names += recursive_directory_walk(subdir)
    return module_names

def regression_test():
    path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../.."
    print path

    modules = map(__import__, recursive_directory_walk(path))
    load = unittest.defaultTestLoader.loadTestsFromModule

    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    unittest.main(defaultTest="regression_test")
