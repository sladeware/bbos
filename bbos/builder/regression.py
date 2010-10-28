"""BBOS Builder Regression testing framework
"""

__copyright__  = "Copyright (c) 2010 Slade Maurer, Alexander Sviridenko"

import os
import re
import sys
import unittest

def regressionTest():
    path = os.path.abspath(os.path.dirname(sys.argv[0]))

    files = os.listdir(path)
    test = re.compile("test\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)

    modules = map(__import__, moduleNames)
    load = unittest.defaultTestLoader.loadTestsFromModule

    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    unittest.main(defaultTest="regressionTest")
