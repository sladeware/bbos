#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.app import Application, Mapping
from bb.os import OS, Kernel, Thread, Port
from bb.hardware.boards import PropellerDemoBoard
from bb.mm.mempool import MemPool, mwrite

import time

class MinimeterOS(OS):

    def __init__(self):
        OS.__init__(self)
        self.init_complete = False
        self.pir_motion_sensor_init_complete = False
        self.iteration_counter = 0
        self.sensor_info = self.SensorInfo()

        # When the next interval begins
        self.start_of_next_interval = 0

        # Unique ID that is a primary key in the database's minimeter table
        self.unique_id = Application.get_running_instance().get_active_mapping().name

        # The record containing statistics on the samples collected
        self.record = "UNIMPLEMENTED"

        # How many samples we collect before sending to the database
        self.SEND_RECORD_THRESHOLD = 30

        # The interval of time in seconds that we wait until next collection
        self.INTER_COLLECTION_WAIT_TIME = 1.0

        # How many sensors are supported on this minimeter
        self.NUMBER_OF_SENSORS = 5

        # The size in bytes of each sensor data record, which includes:
        #   4 Bytes for Sensor Payload Data
        #   1 Bytes for Sensor ID
        #   4 Bytes for linked list next pointer
        #   9 Bytes Total
        # NB: These could be reduced in size if we wanted to
        self.SENSOR_DATA_SIZE_IN_BYTES = 4 + 1 + 4

        # Mempool containing the sensor data that we to store each iteration
        # 30 * 5 * 9B = 1350 Bytes
        self.sensor_mempool = MemPool(self.SEND_RECORD_THRESHOLD *
                                      self.NUMBER_OF_SENSORS,
                                      self.SENSOR_DATA_SIZE_IN_BYTES)

        # The size in bytes of a database record that we are sending
        self.RECORD_SIZE_IN_BYTES = 1 # ??? FILL IN WITH ACTUAL SIZE

        # The number of records we have in flight
        # For now we have two, so that we allow two intervals for a message
        # to be sent and memory freed before running out of memory
        self.NUMBER_OF_RECORDS = 2

        # The head of the list of sensor data allocated from a memory pool
        # This is the first element allocated
        self.sensor_data_head = None

        # The tail of the list of sensor data allocated from a memory pool
        # This is the most recently allocated element
        self.sensor_data_tail = None

        # Mempool containing the records that we to send to the database
        self.sensor_mempool = MemPool(self.RECORD_SIZE_IN_BYTES,
                                      self.NUMBER_OF_RECORDS)

    def __send_record(self):
        """Compute statistics on the data we've collected, create a record,
        encapsulate it in a message and send the message to the receiving
        thread on the remote database system"""
        # Unimplemented
        print "sending record: " + self.record

    def __add_sensor_data(self, data, sensor_id):
        """Add a new sensor data element"""
        sensor_data = self.sensor_mempool.malloc()
        if sensor_data:
            mwrite(sensor_data, self.SensorData())
            sensor_data.sensor_id = sensor_id
            sensor_data.data = data
            if self.sensor_data_head == None:
                self.sensor_data_head = sensor_data
                self.sensor_data_tail = sensor_data
            else:
                self.sensor_data_tail.next_pointer = sensor_data
                self.sensor_data_tail = sensor_data
            print "new sensor data: " + str(sensor_data)
        else:
            print "WARNING: problems allocating memory for sensor data"

    def __collect_sensor_data(self):
        """Read sensor data and store it in linked list for post-processing.
           Data is collected over the interval we waited by the sensors and
           their drivers. We simply poll the drivers to determine max
           values during the waiting interval."""
        # Collect a Hygrometer sample and store it (max humidity)
        print "collecting hygrometer data"
        data = 1234 + self.SEND_RECORD_THRESHOLD # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.HYGROMETER_ID)

        # Collect a Light to Frequency sample and store it (max frequency)
        print "collecting light data"
        data = 1435 + self.SEND_RECORD_THRESHOLD # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.LIGHT_ID)

        # Collect a PIR Motion sample and store it (number of times activated)
        print "collecting motion data"
        data = 5324 + self.SEND_RECORD_THRESHOLD # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.MOTION_ID)

        # Collect a Microphone Sound sample and store it (max amplitude)
        print "collecting sound data"
        data = 5512 + self.SEND_RECORD_THRESHOLD # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.SOUND_ID)

        # Collect a Temperature sample and store it (max temperature in Celsius)
        print "collecting temperature data"
        data = 8767 + self.SEND_RECORD_THRESHOLD # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.TEMPERATURE_ID)

    def __create_record(self):
        """Create a record from the statistics generated on the sensor data"""
        print "creating the database record"
        #UNIMPLEMENTED

    def __post_processing(self):
        """Compute statistics from sensor data and create a database record"""
        print "post processing"

        # Iterate over all data sampled during the last interval
        sensor_data = self.sensor_data_head
        while sensor_data:
            self.sensor_info.compute(sensor_data)
            old_sensor_data = sensor_data
            sensor_data = sensor_data.next_pointer
            self.sensor_mempool.free(old_sensor_data)

        # Create the record
        self.__create_record()

        # Cleanup sensor data linked list
        self.sensor_data_head = None
        self.sensor_data_tail = None

        # Cleanup intermediate working variables
        self.sensor_info.cleanup()

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
        print "Sensor processor running: " + str(self.iteration_counter)
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
        self.kernel.load_module("bb.os.drivers.net.wireless.xbee")

    class SensorInfo():
        """DDO containing information about the sensors on this minimeter"""
        UNASSIGNED_ID  = 0
        HYGROMETER_ID  = 1
        LIGHT_ID       = 2
        MOTION_ID      = 3
        SOUND_ID       = 4
        TEMPERATURE_ID = 5

        h_ctr = 0
        l_ctr = 0
        m_ctr = 0
        s_ctr = 0
        t_ctr = 0

        h_max = 0
        l_max = 0
        m_max = 0
        s_max = 0
        t_max = 0

        h_sum = 0
        l_sum = 0
        m_sum = 0
        s_sum = 0
        t_sum = 0

        def compute(self, sensor_data):
            """Compute statistics from the sensor data"""
            print "computing stats from: " + str(sensor_data)
            if sensor_data.sensor_id == self.HYGROMETER_ID:
                self.h_ctr += 1
                if self.h_max < sensor_data.data:
                    self.h_max = sensor_data.data
                self.h_sum += sensor_data.data
            if sensor_data.sensor_id == self.LIGHT_ID:
                self.l_ctr += 1
                if self.sensorl_info._max < sensor_data.data:
                    self.sensorl_info._max = sensor_data.data
                self.l_sum += sensor_data.data
            if sensor_data.sensor_id == self.MOTION_ID:
                self.m_ctr += 1
                if self.m_max < sensor_data.data:
                    self.m_max = sensor_data.data
                self.m_sum += sensor_data.data
            if sensor_data.sensor_id == self.SOUND_ID:
                self.s_ctr += 1
                if self.s_max < sensor_data.data:
                    self.s_max = sensor_data.data
                self.s_sum += sensor_data.data
            if sensor_data.sensor_id == self.TEMPERATURE_ID:
                self.t_ctr += 1
                if self.t_max < sensor_data.data:
                    self.t_max = sensor_data.data
                self.t_sum += sensor_data.data

        def cleanup(self):
            """Cleanup all the intermediate working variables used for stats"""
            print "cleaning up stats"
            self.h_ctr = 0
            self.h_max = 0
            self.h_sum = 0
            self.l_ctr = 0
            self.l_max = 0
            self.l_sum = 0
            self.m_ctr = 0
            self.m_max = 0
            self.m_sum = 0
            self.s_ctr = 0
            self.s_max = 0
            self.s_sum = 0
            self.t_ctr = 0
            self.t_max = 0
            self.t_sum = 0

    class SensorData():
        data = 0
        sensor_id = 0
        next_pointer = None

        def __str__(self):
            return "data:" + str(data) + " id" + str(sensor_id) + "next:"
            + str(next_pointer)

class MinimeterBoard(PropellerDemoBoard):
    """Let us use for the first time Propeller Demo Board as the board for
    minimeter. On the next step we can create a special board by using Board
    class."""

class Minimeter(Mapping):
    """This class aims to describe minimeter device. The name of each device has
    the following template: M<ID>."""
    def __init__(self, id):
        Mapping.__init__(self, name="M%d" % id, os_class=MinimeterOS)
