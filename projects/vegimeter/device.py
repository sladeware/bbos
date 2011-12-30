#!/usr/bin/env python

import os.path
import getpass

from bb.hardware.compatibility import Fritzing
from bb.hardware.primitives import Pin
from bb.utils import module

# Provide environment setup for each developer
if getpass.getuser() == "d2rk":
    Fritzing.set_home_dir("/opt/fritzing")
Fritzing.add_search_path(os.path.join(module.get_dir(), "parts"))

vegimeter_device = Fritzing.parse("device.fz")
#for element in vegimeter_device.get_elements():
#    print element.get_property_value("name"), element.designator

ts1 = vegimeter_device.find_element("DS18B20_1")
for pin in ts1.find_elements(Pin):
    print pin.get_property_value("name"), pin.designator
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
