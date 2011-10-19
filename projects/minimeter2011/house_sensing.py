#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This application describes a network of minimeters to be used as a house
sensing system."""

import bb.simulator
from bb.app import Application, Mapping
from bb.os import OS, Kernel, Thread, Port
from bb.hardware.boards import PropellerDemoBoard

import time

class MinimeterOS(OS):
    """This class describes operating system that will control each minimeter
    device."""
    def __init__(self):
        OS.__init__(self)
        self.init_complete = False
        self.pir_motion_sensor_init_complete = False

    def initializer(self):
        """The purpose of this runner is to initialize the minimeter: open
        PIR motion detector sensor, mic, XBEE wireless module, light level
        sensor, hygrometer, temp sensor."""
        # Check the initialization flag first. Skip initialization part if it
        # was already complete.
        if self.init_complete:
            return
        # Continue minimeter initialization, something wasn't open yet
        self.kernel.echo("Continue initialization...")
        # Open PIR motion sensor
        if not self.pir_motion_sensor_init_complete and \
                self.kernel.control_device("PIR_MOTION_SENSOR_DEVICE", "open", 1<<7):
            self.kernel.echo("PIR motion sensor has been opened (pin 7)")
            self.pir_motion_sensor_init_complete = True
        # Check whether all minimeter parts were initialized. If so, finish the
        # initialization.
        if self.pir_motion_sensor_init_complete:
            self.kernel.echo("Initialization complete")
            self.init_complete = True
        time.sleep(1)

    def main(self):
        self.kernel.add_port(Port("INITIALIZER_PORT", 10))
        self.kernel.add_thread(Thread("INITIALIZER", self.initializer,
            "INITIALIZER_PORT"))
        self.kernel.load_module("bb.os.drivers.sensors.pir_sensor")

class MinimeterBoard(PropellerDemoBoard):
    """Let us use for the first time Propeller Demo Board as the board for
    minimeter. On the next step we can create a special board by using Board
    class."""

class Minimeter(Mapping):
    """This class aims to describe minimeter device. The name of each device has
    the following template: M<ID>."""
    def __init__(self, id):
        Mapping.__init__(self, name="M%d" % id, os_class=MinimeterOS)

minimeter1 = Minimeter(1)
minimeter_board1 = MinimeterBoard([minimeter1])

# Just another minimeter device. Put it to the application right beside
# minimeter1 and you will have a network of minimeters :)
minimeter2 = Minimeter(2)
minimeter_board2 = MinimeterBoard([minimeter2])

house_sensing = Application([minimeter1])
house_sensing.start()
