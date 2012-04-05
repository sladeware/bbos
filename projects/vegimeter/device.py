#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import os.path
import getpass

from bb.hardware.design import Network
from bb.hardware.compatibility import Fritzing
from bb.hardware.primitives import Pin
from bb.utils import module

# Provide environment setup for each developer
Fritzing.set_home_dir("/opt/fritzing")
Fritzing.add_search_path(os.path.join(module.get_dir(), "parts"))

vegimeter_device = Fritzing.parse("device.fz")
#for element in vegimeter_device.get_elements():
#    print element.get_property_value("name"), element.designator

import networkx
#from bb.hardware.primitives import G

quickstart = vegimeter_device.find_element("QSP1")
tempsensor1 = vegimeter_device.find_element("TS1")

#print "Connections of TS1 with QSB1"
#for src_pin in tempsensor1.find_elements(Pin):
#    for dst_pin in quickstart.find_elements(Pin):
#        res = networkx.bidirectional_dijkstra(G, src_pin, dst_pin)
#        if res:
#            length, path = res
#            print "%s (%s) ==> %s (%s)" \
#                % (src_pin.get_property_value("name"), src_pin.designator,
#                   dst_pin.get_property_value("name"), dst_pin.designator)
#exit(0)

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
