#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

"""This application describes a network of minimeters to be used as a house
sensing system."""

from bb import simulator
from bb.app import Application, Mapping
from bb.os import OS, Kernel, Thread, Port
from bb.hardware.boards import PropellerDemoBoard
from bb.mm.mempool import MemPool

import time

class MinimeterOS(OS):

    def __init__(self):
        OS.__init__(self)
        self.init_complete = False
        self.pir_motion_sensor_init_complete = False
        self.iteration_counter = 0

        # When the next interval begins
        self.start_of_next_interval = 0

        # The list of sensor data allocated from a memory pool
        self.sensor_data_list = None

        # Unique ID that is a primary key in the database's minimeter table
        self.unique_id = Application.get_running_instance().get_active_mapping().name

        # The record containing statistics on the samples collected
        self.record = "UNIMPLEMENTED"

        # How many samples we collect before sending to the database
        self.SEND_RECORD_THRESHOLD = 60

        # The interval of time in seconds that we wait until next collection
        self.INTER_COLLECTION_WAIT_TIME = 1.0

        # How many sensors are supported on this minimeter
        self.NUMBER_OF_SENSORS = 5

        # The size in bytes of each sensor data record, which includes:
        #   4 Bytes for Sensor Payload Data
        #   1 Bytes for Sensor ID
        #   4 Bytes for linked list next pointer
        #   9 Bytes Total
        self.SENSOR_DATA_SIZE_IN_BYTES = 4 + 1 + 4

        # Mempool containing the sensor data that we to store each iteration
        self.sensor_mempool = MemPool(self.SEND_RECORD_THRESHOLD *
                                      self.NUMBER_OF_SENSORS,
                                      self.SENSOR_DATA_SIZE_IN_BYTES)

        # The size in bytes of a database record that we are sending
        self.RECORD_SIZE_IN_BYTES = 1 # ??? FILL IN WITH ACTUAL SIZE

        # The number of records we have in flight
        # For now we have two, so that we allow two intervals for a message
        # to be sent and memory freed before running out of memory
        self.NUMBER_OF_RECORDS = 2

        # Mempool containing the records that we to send to the database
        self.sensor_mempool = MemPool(self.RECORD_SIZE_IN_BYTES,
                                      self.NUMBER_OF_RECORDS)

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
        """Read sensor data and store it in linked list for post-processing.
           Data is collected over the interval we waited by the sensors and
           their drivers. We simply poll the drivers to determine max
           values during the waiting interval."""
        # Collect a Hygrometer sample and store it (max humidity)
        self.__print("collecting hygrometer data")

        # Collect a Light to Frequency sample and store it (max frequency)
        self.__print("collecting light data")

        # Collect a PIR Motion sample and store it (number of times activated)
        self.__print("collecting motion data")

        # Collect a Microphone Sound sample and store it (max amplitude)
        self.__print("collecting sound data")

        # Collect a Temperature sample and store it (max temperature in Celsius)
        self.__print("collecting temperature data")

    def __post_processing(self):
        """Compute statistics from sensor data and create a database record"""
        # Unimplemented
        self.__print("post processing")

    def sensor_processor(self):
        """Main part of the appliction that processes sensor data."""
        # Do nothing if we have not been initialized
        if self.init_complete != True:
            return

        # Wait (non-blocking) until the next sampling iterval
        now = time.time()
        if time.time() < self.start_of_next_interval:
            return
        else:
            self.start_of_next_interval = now + self.INTER_COLLECTION_WAIT_TIME

        # Collect this iteration's sensor data
        self.iteration_counter += 1
        self.__print("Sensor processor running: " + str(self.iteration_counter))
        self.__collect_sensor_data()

        # If we have enough data, send the record to the database for storage
        if self.iteration_counter > self.SEND_RECORD_THRESHOLD:
            self.__post_processing()
            self.__send_record()
            self.iteration_counter = 0

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
                self.kernel.control_device("PIR_MOTION_SENSOR_DEVICE",
                                           "open", 1<<7):
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

    class SensorInfo():
        """DDO containing information about the sensors on this minimeter"""
        HYGROMETER_ID  = 0
        LIGHT_ID       = 1
        MOTION_ID      = 2
        SOUND_ID       = 3
        TEMPERATURE_ID = 4
        
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

if __name__ == '__main__':
    simulator.config.parse_command_line()
    house_sensing.start()
