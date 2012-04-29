#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.app import appmanager

import vegimeter

vegetable_plant_guard = appmanager.new_application([vegimeter.Vegimeter()])
vegetable_plant_guard.add_device(vegimeter.vegimeter_device)
vegetable_plant_guard.start()
