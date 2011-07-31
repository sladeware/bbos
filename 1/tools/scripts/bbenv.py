#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import os
import os.path
import sys

SCRIPT_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Setup the path properly for bbos builder imports 
_extra_paths = []

# Define BBHOME environment variable
if not os.environ.has_key('BBHOME'):
    os.environ['BBHOME'] = os.path.join(SCRIPT_DIR, '..', '..')
_extra_paths.append(os.environ['BBHOME'])

# Add libraries
_extra_paths.append(
    os.path.join(os.environ['BBHOME'], 'lib', 'python', 'module'),
)

# Fix the sys.path to include our extra paths
sys.path = _extra_paths + sys.path

