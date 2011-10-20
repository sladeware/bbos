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

    def __init__(self):
        OS.__init__(self)
        self.init_complete = False
        self.pir_motion_sensor_init_complete = False
        self.iteration_counter = 0

        # Unique ID that is a primary key in the database's minimeter table
        self.unique_id = Application.get_running_instance().get_active_mapping().name

        # The record containing statistics on the samples collected
        self.record = "UNIMPLEMENTED"

        # How many samples we collect before sending to the database
        self.SEND_RECORD_THRESHOLD = 60

        # The amount of time we sleep collecting samples
        self.INTER_COLLECTION_SLEEP_TIME = 1

    def __print(self, data):
        """Print out the data to the terminal with appropriate breadcrumbs."""
        self.kernel.echo(self.unique_id + " : " + data)

    def __send_record(self):
        """Compute statistics on the data we've collected, create a record,
        encapsulate it in a message and send the message to the receiving
        thread on the remote database system"""
        # Unimplemented
        self.__print("sending record: " + self.record)

    def __collect_sensor_data(self):
        """Read sensor data and store it in arrays for post-processing"""
        # Unimplemented
        self.__print("collecting sensor data")

    def __post_processing(self):
        """Compute statistics from sensor data and create a database record"""
        # Unimplemented
        self.__print("post processing")

    def sensor_processor(self):
        """This is the main part of the appliction that processes sensor data."""
        # Do nothing if we have not been initialized
        if self.init_complete != True:
            return

        # Collect this iteration's sensor data
        self.iteration_counter += 1
        self.__print("Sensor processor running: " + str(self.iteration_counter))
        self.__collect_sensor_data()

        # If we have enough data, send the record to the database for storage
        if self.iteration_counter > self.SEND_RECORD_THRESHOLD:
            self.__post_processing()
            self.__send_record()
            self.iteration_counter = 0

        # Sleep until the next iteration should begin
        time.sleep(self.INTER_COLLECTION_SLEEP_TIME)

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
        else:
            time.sleep(1)

    def main(self):
        # The sensor_processor thread won't do anything until the initializer
        # thread is complete. The initializer thread does nothing after it is
        # complete. For this reason, we can safely reuse this port.
        self.kernel.add_port(Port("PRIMARY_PORT", 10))
        self.kernel.add_thread(Thread("INITIALIZER", self.initializer,
            "PRIMARY_PORT"))
        self.kernel.add_thread(Thread("SENSOR_PROCESSOR", self.sensor_processor,
            "PRIMARY_PORT"))
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

# Note that there is not a direct connection between minimeters. They can only
# communicate with the database via wireless transmission.
house_sensing = Application([minimeter1, minimeter2])
house_sensing.start()
