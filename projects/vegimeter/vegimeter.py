#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

#_______________________________________________________________________________

import os

from bb.tools import Fritzing
from bb.utils import module

#_______________________________________________________________________________
# Vegimeter device

# First of all we need to setup Fritzing
Fritzing.set_home_dir("/opt/fritzing")
Fritzing.add_search_path(os.path.join(module.get_dir(), "parts"))

# Note, this may take some time
vegimeter_device = Fritzing.parse("device.fz")

def bill_of_materials():
    bill_of_materials = dict()
    for element in vegimeter_device.get_elements():
        name = element.get_property_value("name")
        if name not in bill_of_materials:
            bill_of_materials[name] = 0
        bill_of_materials[name] += 1
    return bill_of_materials

#_______________________________________________________________________________

if __name__ == "__main__":
    print "Vegimeter bill of materials:"
    for name, amount in bill_of_materials().items():
        print "\t%d %s(s)" % (amount, name)
