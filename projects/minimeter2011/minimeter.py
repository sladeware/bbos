#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

from bb.app import Application, Mapping
from bb.os import OS, Kernel, Thread, Port
from bb.mm.mempool import MemPool, mwrite
from bb.hardware.boards import PropellerDemoBoard
from bb.hardware.net.wireless.xbee import XBee
from bb.hardware.leds import LED

import time

class MinimeterOS(OS):
    """This class describes operating system that controls a single minimeter
    device."""

    def __init__(self, verbose=True):
        """Setting verbose to False produces database records that contain
        the stats only and not all of the data collected during the recording
        interval. Defaults to True."""
        OS.__init__(self)
        self.init_complete = False
        self.pir_motion_sensor_init_complete = False
        self.iteration_counter = 0
        self.sensor_info = self.SensorInfo()

        # When the next interval begins
        self.start_of_next_interval = 0

        # Unique ID that is a primary key in the database's minimeter table
        self.unique_id = hash(
            Application.get_running_instance().get_active_mapping().name)

        # The record containing statistics on the samples collected
        self.record = None

        # How many samples we collect before sending to the database
        self.SEND_RECORD_THRESHOLD = 30

        # The interval of time in seconds that we wait until next collection
        self.INTER_COLLECTION_WAIT_TIME = 1.0

        # How many sensors are supported on this minimeter
        self.NUMBER_OF_SENSORS = 5

        # The size in bytes of each sensor data record, which includes:
        #    4 Bytes for Sensor Payload Data
        #    1 Bytes for Sensor ID
        #    4 Bytes for linked list next pointer
        #    9 Bytes Total
        # NB: These could be reduced in size if we wanted to
        self.SENSOR_DATA_SIZE_IN_BYTES = 4 + 1 + 4

        # Mempool containing the sensor data that we to store each iteration
        # 30 * 5 * 9B = 1350 Bytes
        self.sensor_mempool = MemPool((self.SEND_RECORD_THRESHOLD + 1) *
                                      self.NUMBER_OF_SENSORS,
                                      self.SENSOR_DATA_SIZE_IN_BYTES)

        # The size in bytes of a database record that we are sending
        #    4 Bytes minimeter unique id
        #    4 Bytes database record generation ID
        #    4 Bytes hygrometer max value
        #    4 Bytes hygrometer mean value
        #    4 Bytes light max value
        #    4 Bytes light mean value
        #    4 Bytes motion max value
        #    4 Bytes motion mean value
        #    4 Bytes sound max value
        #    4 Bytes sound mean value
        #    4 Bytes temperature max value
        #    4 Bytes temperature mean value
        #    48 Bytes Total
        self.RECORD_SIZE_IN_BYTES = 4 * 12

        # The number of records we have in flight
        self.NUMBER_OF_RECORDS = 1

        # The head of the list of sensor data allocated from a memory pool
        # This is the first element allocated
        self.sensor_data_head = None

        # The tail of the list of sensor data allocated from a memory pool
        # This is the most recently allocated element
        self.sensor_data_tail = None

        # Enable verbose records, which include all sensor data and stats
        self.VERBOSE = verbose

        # Mempool containing the records that we to send to the database
        # It is appended to the stats record and contains (data, sensor_id)
        # pairs as they were recorded by the minimeter.
        record_size = self.RECORD_SIZE_IN_BYTES
        if self.VERBOSE:
            # The number of pairs in the verbose record
            num_pairs = self.SEND_RECORD_THRESHOLD + 1
            # A pair is the 4B data and 1B sensor_id
            record_size += num_pairs * self.NUMBER_OF_SENSORS * (4 + 1)
            # Total 823 Bytes = 48B + (31 * 5 * (4B + 1B))
        self.record_mempool = MemPool(record_size, self.NUMBER_OF_RECORDS)

    def __send_record(self):
        """Compute statistics on the data we've collected, create a record,
        encapsulate it in a message and send the message to the receiving
        thread on the remote database system"""
        # Unimplemented
        print "sending record: "
        for field in self.record[:]:
            print str(field)
        self.record_mempool.free(self.record)

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
        data = 1234 + self.iteration_counter # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.HYGROMETER_ID)

        # Collect a Light to Frequency sample and store it (max frequency)
        print "collecting light data"
        data = 1435 + self.iteration_counter # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.LIGHT_ID)

        # Collect a PIR Motion sample and store it (number of times activated)
        print "collecting motion data"
        data = 5324 + self.iteration_counter # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.MOTION_ID)

        # Collect a Microphone Sound sample and store it (max amplitude)
        print "collecting sound data"
        data = 5512 + self.iteration_counter # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.SOUND_ID)

        # Collect a Temperature sample and store it (max temperature in Celsius)
        print "collecting temperature data"
        data = 8767 + self.iteration_counter # TODO: Get data from driver
        self.__add_sensor_data(data, self.SensorInfo.TEMPERATURE_ID)

    def __create_record(self):
        """Create a record from the statistics generated on the sensor data"""
        print "creating the database record"
        self.record = self.record_mempool.malloc()
        if self.record:
            array = [self.unique_id,
                     self.sensor_info.DATABASE_GENERATION_ID,
                     self.sensor_info.h_max,
                     int(float(self.sensor_info.h_sum) /
                         float(self.sensor_info.h_ctr)),
                     self.sensor_info.l_max,
                     int(float(self.sensor_info.l_sum) /
                         float(self.sensor_info.l_ctr)),
                     self.sensor_info.m_max,
                     int(float(self.sensor_info.m_sum) /
                         float(self.sensor_info.m_ctr)),
                     self.sensor_info.s_max,
                     int(float(self.sensor_info.s_sum) /
                         float(self.sensor_info.s_ctr)),
                     self.sensor_info.t_max,
                     int(float(self.sensor_info.t_sum) /
                         float(self.sensor_info.t_ctr))
                     ]
            if self.VERBOSE:
                sensor_data = self.sensor_data_head
                while sensor_data:
                    array.append(int(sensor_data.data))
                    array.append(int(sensor_data.sensor_id))
                    sensor_data = sensor_data.next_pointer
            mwrite(self.record, array)

    def __post_processing(self):
        """Compute statistics from sensor data and create a database record"""
        print "post processing"

        # Iterate over all data sampled during the last interval
        sensor_data = self.sensor_data_head
        while sensor_data:
            self.sensor_info.compute(sensor_data)
            sensor_data = sensor_data.next_pointer

        # Create the record
        self.__create_record()

        # Cleanup sensor data linked list
        sensor_data = self.sensor_data_head
        while sensor_data:
            old_sensor_data = sensor_data
            sensor_data = sensor_data.next_pointer
            self.sensor_mempool.free(old_sensor_data)
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
        """Container for information about the sensors on this minimeter. Also,
        able to compute statistics about sensor data."""
        UNASSIGNED_ID  = 0
        HYGROMETER_ID  = 1
        LIGHT_ID       = 2
        MOTION_ID      = 3
        SOUND_ID       = 4
        TEMPERATURE_ID = 5

        # All records of the same generation have identical columns
        DATABASE_GENERATION_ID = 1

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
                if self.l_max < sensor_data.data:
                    self.l_max = sensor_data.data
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

    class SensorData(object):
        data = 0
        sensor_id = 0
        next_pointer = None

        def __str__(self):
            return ' '.join(("data=" + str(self.data),
                             "id=" + str(self.sensor_id),
                             "next=" + str(self.next_pointer)))

class MinimeterDevice(PropellerDemoBoard):
    """This class describes minimeter device.

    Let us use for the first time  Propeller Demo Board as the board for
    minimeter. On the next step we can create a special board by using Board
    class."""
    def __init__(self, minimeter):
        PropellerDemoBoard.__init__(self, [minimeter])
        self.add_device(XBee())
        self.add_device(LED(color=LED.GREEN))
        self.add_device(LED(color=LED.RED))
        self.add_device(LED(color=LED.YELLOW))

class Minimeter(Mapping):
    """This class aims to describe minimeter device. The name of each device has
    the following template: M<ID>."""
    def __init__(self, id, build_params=None):
        Mapping.__init__(self, name="M%d" % id, os_class=MinimeterOS,
                         build_params=build_params)
        MinimeterDevice(self)

if __name__ == "__main__":
    print "Demonstration"
    minimeter = Minimeter(1)
    print "Demo minimeter device consists of the following parts:"
    counter = 0
    for device in minimeter.hardware.get_board().get_devices():
        counter += 1
        print "%d. %s" % (counter, str(device))
