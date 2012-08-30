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

__copyright__ = 'Copyright (c) 2012 Sladeware LLC'

import re
import os.path

import bb
from bb.hardware.primitives import Pin
from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A_Q44

# Temporary flag in order to hide fritzing support from users.
USE_FRITZING = False

if USE_FRITZING:
  from bb.third_party import fritzing

  # First of all you need to setup Fritzing
  # NOTE(team): developer can use fritzing.set_home_dir() to setup home
  # directory directly.
  fritzing.find_home_dir()
  fritzing.add_search_path(os.path.join(bb.env.pwd(), 'parts'))
  vegimeter_device = fritzing.parse('device.fz')
  # Fix vegimeter device design loaded from Fritzing schematic. The reason is
  # that the current version of QuickStart Board doesn't have a parts such as
  # Propeller P8X32A-Q44 microchip. Thus we need to add them manually.
  board = vegimeter_device.find_element('QSP1')
  processor = board.add_element(PropellerP8X32A_Q44())
  processor.set_designator('PRCR1')
else:
  from bb.hardware.devices.boards import P8X32A_QuickStartBoard
  board = P8X32A_QuickStartBoard()
  board.set_designator('QSP1')
  processor = board.add_element(PropellerP8X32A_Q44())
  processor.set_designator('PRCR1')
  vegimeter_device = board

vegimeter_board = None
if vegimeter_device.get_designator() == 'QSP1':
  vegimeter_board = vegimeter_device
else:
  vegimeter_board = vegimeter_device.find_element('QSP1')
if not vegimeter_board:
  print "Board <QSP1> cannot be found!"
  exit(0)

vegimeter = bb.Mapping('Vegimeter', board=vegimeter_board)
vegimeter.register_thread(bb.os.Thread('UI', 'ui_runner'))
vegimeter.register_thread(bb.os.Thread('CONTROL_PANEL', 'control_panel_runner'))

# TODO(team): the following (and others) drivers has to be connected
# automatically.
from bb.os.drivers.gpio.button_driver import ButtonDriver
from bb.os.drivers.processors.propeller_p8x32 import ShMemDriver
vegimeter.register_threads([ButtonDriver(), ShMemDriver()])

def bill_of_materials():
  bill_of_materials = dict()
  for element in vegimeter_device.get_elements():
    name = element.get_property_value('name')
    if name not in bill_of_materials:
      bill_of_materials[name] = 0
    bill_of_materials[name] += 1
  return bill_of_materials

if __name__ == '__main__':
  print 'Vegimeter bill of materials:'
  for name, amount in bill_of_materials().items():
    print "\t%d %s(s)" % (amount, name)

"""
## The next snippet shows all the pins
#pins = tempsensor1.find_elements(Pin)
#for pin in pins:
#    print pin.get_property_value("name")

def get_quickstartboard_pin_designator(name):
    mapping = {
        33 : 34, 32 : 33, 21 : 18, 7 : 8, 26 : 28, 2 : 3, 17 : 38,
        1 : 2, 18 : 39, 30 : 32, 16 : 37, 25 : 27, 27 : 29, 28 : 30,
        40 : 26, 14 : 15, 20 : 17, 24 : 21, 10 : 11, 31 : 16, 11 : 12,
        22 : 19, 0 : 1, 23 : 20, 13 : 14, 29 : 31, 6 : 7, 39 : 25,
        3 : 4, 36 : 22, 9 : 10, 12 : 13, 15 : 36, 8 : 9, 38 : 24,
        4 : 5, 34 : 35, 37 : 23, 19 : 40, 5 : 6
        }
    m = re.match(r"connector(\d+)", name)
    return mapping[int(m.group(1))]

print "Connections of TS1 with QSB1"
for src_pin in tempsensor1.find_elements(Pin):
    for dst_pin in quickstart.find_elements(Pin):
        res = networkx.bidirectional_dijkstra(G, src_pin, dst_pin)
        if res:
            length, path = res
            print "%s (%s) ==> %s (%s)" \
                % (src_pin.get_property_value("name"),
                   get_quickstartboard_pin_designator(src_pin.designator),
                   dst_pin.get_property_value("name"),
                   get_quickstartboard_pin_designator(dst_pin.designator))

import networkx
from bb.hardware.primitives import G

quickstart = vegimeter_device.find_element("QSP1")
tempsensor1 = vegimeter_device.find_element("TS1")
"""
