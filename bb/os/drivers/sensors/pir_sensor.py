#!/usr/bin/env python

__copyright__ = "Copyright (C) 2011 Sladeware LLC"

from bb.os import Driver, Device, get_running_kernel

class PIRMotionSensorDevice(Device):
    name="PIR_MOTION_SENSOR_DEVICE"

class PIRMotionSensorDriver(Driver):
    name="PIR_MOTION_SENSOR_DRIVER"
    version="0.0.0"

    def init(self):
        pass

    def open(self, output_pin):
        return get_running_kernel().control_device("PROPELLER_P8X32_GPIO_DEVICE",
                                            "open", output_pin)

def on_load():
    pir_sensor = PIRMotionSensorDevice()
    pir_sensor.driver = get_running_kernel().register_driver(PIRMotionSensorDriver)
    get_running_kernel().register_device(pir_sensor)

def on_unload():
    get_running_kernel().unregister_driver(PIRMotionSensorDriver)
