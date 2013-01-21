#!/usr/bin/env python

# Skip bbapp automatic installation for now

import bb
from bb.utils import path_utils

location = path_utils.dirname(path_utils.realpath(__file__))
print "Update user config"
bb.user_config.set("bbos", "location", location)
bb.user_config.write()
