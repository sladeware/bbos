#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This application describes a network of minimeters to be used as a house
sensing system."""

from bb import simulator
from bb.app import Application
from minimeter import Minimeter, MinimeterBoard

minimeter1 = Minimeter(1)
minimeter_board1 = MinimeterBoard([minimeter1])

# Just another minimeter device. Put it to the application right beside
# minimeter1 and you will have a network of minimeters :)
minimeter2 = Minimeter(2)
minimeter_board2 = MinimeterBoard([minimeter2])

# Note that there is not a direct connection between minimeters. They can only
# communicate with the database via wireless transmission.
house_sensing = Application([minimeter1, minimeter2],
                            mappings_execution_interval=3)

if __name__ == '__main__':
    simulator.config.parse_command_line()
    house_sensing.start()
