
****************************
Writing simple device driver
****************************

The device driver is represented by :class:`bb.os.kernel.Driver` class and aims
to control device that is derived from :class:`bb.hardware.devices.device.Device` class. 

=================
Creating a device
=================

If you already have a serial device that you would like to control, then you
can skip this part. Otherwise, follow the next instructions to create a
simple serial device to test serial driver.

Create a simple serial device that will be controled by our driver
:class:`MySerialDriver`. The device class should be derived from the base device
class :class:`bb.hardware.devices.device.Device` and will have such designator
format, that ``MY_SERIAL_DEV1``, ``MY_SERIAL_DEV2``, etc. Now we are ready::

    from bb.hardware.devices import Device
    from my_serial_driver import MySerialDriver

    class MySerialDevice(Device):
        DEFAULT_DRIVER_CLASS=MySerialDriver
        DEFAULT_DESIGNATOR_FORMAT="MY_SERIAL_DEV%d"

Once the device was created we can connected with other devices.

================
Writing a driver
================

Basically each new driver lives in a module. Thus, first of all you need learn
how to write simple module.

Let us start to create a new driver ``my_serial_driver``.

Let us assume, we would like to create a new serial driver and. The basic
commands are:

* ``serial_open``
* ``serial_close``
* ``serial_read``
* ``serial_write``

A::

    from bb.os.drivers.serial import SerialDriver

    class MySerialDriver(SerialDriver):
        name="MY_SERIAL_DRIVER"

        @SerialDriver.action_handler
        def serial_open(self):
            pass
        
        @SerialDriver.action_handler
        def serial_close(self):
            pass
        
        @SerialDriver.action_handler
        def serial_read(self):
            pass
        
        @SerialDriver.action_handler
        def serial_write(self):
            pass

Now once driver was created we need to finilize the module::

    def on_load():
        get_running_kernel().register_driver(MySerialDriver)

    def on_unload():
        get_running_kernel().unregister_driver(MySerialDriver)
        
============
Using driver
============

Now we can use our new serial driver :class:`MySerialDriver`. First of all
we need to load the ``my_serial_driver`` module::

    get_running_kernel().load_module("my_serial_driver")

Now we can control device and write::

    get_running_kernel().control_device("MY_SERIAL_DRIVER")




