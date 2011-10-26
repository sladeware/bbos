#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This application describes a network of minimeters to be used as a house
sensing system."""

from bb import simulator
from bb.app import Application
from minimeter import Minimeter
from workstation import Workstation

# Define workstation that will receive data from minimeter devices.
workstation = Workstation("Workstation")

minimeter1 = Minimeter(1)

# Just another minimeter device. Put it to the application right beside
# minimeter1 and you will have a network of minimeters :)
minimeter2 = Minimeter(2, build_params=dict(verbose=False))

# Note that there is not a direct connection between minimeters. They can only
# communicate with the database via wireless transmission.
# Note that order of mappings is not important. Simulator uses random execution
# order.
# XXX: do we need to make it as an options?
house_sensing = Application([workstation, minimeter1, minimeter2],
                            mappings_execution_interval=2)

if __name__ == '__main__':
    simulator.config.parse_command_line()
    house_sensing.start()
