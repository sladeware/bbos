#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

from bb.app import appmanager

import vegimeter

mappings = [vegimeter.ui, vegimeter.button_driver]
vegetable_plant_guard = appmanager.new_application(mappings)
vegetable_plant_guard.add_device(vegimeter.vegimeter_device)
vegetable_plant_guard.start()
