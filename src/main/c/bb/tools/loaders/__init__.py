#!/usr/bin/env python

"""This package provides loaders support.

List of supported loaders:

   ================================================ ============================
   Loader                                           Brief description
   ================================================ ============================
   :class:`bb.tools.loaders.bstl.BSTLLoader`        BSTL loader
   ================================================ ============================
"""

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'
__author__ = 'Oleksandr Sviridenko'

from bb.tools.loaders.loader import Loader
from bb.tools.loaders.bstl import BSTLLoader
