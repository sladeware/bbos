#!/usr/bin/env python

import os.path
import getpass

from bb.hardware.compatibility import Fritzing
from bb.utils import module

# Provide environment setup for each developer
if getpass.getuser() == "d2rk":
    Fritzing.set_home_dir("/opt/fritzing")
Fritzing.add_search_path(os.path.join(module.get_dir(), "parts"))

vegimeter_device = Fritzing.parse("device.fz")
#for element in vegimeter_device.get_elements():
#    print element.get_property_value("name"), element.designator

print vegimeter_device.find_element("R1")
exit(0)

def bill_of_materials():
    bill_of_materials = dict()
    for element in vegimeter_device.get_elements():
        name = element.get_property_value("name")
        if name not in bill_of_materials:
            bill_of_materials[name] = 0
        bill_of_materials[name] += 1
    return bill_of_materials

print "Vegimeter bill of materials:"
for name, amount in bill_of_materials().items():
    print "\t%d %s(s)" % (amount, name)
