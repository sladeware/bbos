#!/usr/bin/env python

from bb import simulator
from vegetable_plant_guard import vegetable_plant_guard

simulator.config.parse_command_line()
simulator.set_application(vegetable_plant_guard)
simulator.start()
