#!/usr/bin/env python

# There is a local os module inside the bb directory. To access the
# standard library will be used Absolute/Relative imports, available
# with Python 2.5 and upward. 
# See http://docs.python.org/whatsnew/2.5.html#pep-328 for more details.
from __future__ import absolute_import

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os.path
import sys
import types

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bbos builder imports 
_extra_paths = []

# Define BB_HOME environment variable
if not os.environ.has_key('BB_HOME'):
    os.environ['BB_HOME'] = os.path.join(SCRIPT_DIR, '..')

# Add libraries
_extra_paths = [
    os.path.join(os.environ['BB_HOME'], 'lib', 'python', 'module'),
    os.path.join(os.environ['BB_HOME'], 'lib', 'python', 'pyserial-2.5'),
]

# Fix the sys.path to include our extra paths
sys.path = _extra_paths + sys.path

