#!/usr/bin/env python

from __future__ import absolute_import

#_______________________________________________________________________________

try:
    from networkx import *
except ImportError:
    print >>sys.stderr, "Please install networkx library:", \
        "http://networkx.lanl.gov"
    exit(1)

#_______________________________________________________________________________
