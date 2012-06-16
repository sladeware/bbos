
****************************
Writing simple device driver
****************************

The device driver is represented by :class:`bb.os.kernel.Driver` class and aims
to control device that is derived from :class:`bb.hardware.devices.device.Device` class. 

================
Writing a driver
================

Basically each new driver lives in a module. Thus, first of all you need learn
how to write simple module.

Let us start to create a new driver ``my_serial_driver`` that will be able to
control our serial devices. Assume driver's basic commands:

================  ========================
Command           Description
================  ========================
``serial_open``   Open serial connection
``serial_close``  Close serial connection
``serial_read``   Read from the serial
``serial_write``  Write to the serial
================  ========================

Note, driver class should be derived from the base driver class
:class:`bb.os.kernel.Driver`. All the actions have to be marked with
help of :func:`bb.os.kernel.Driver.action_handler` decorator. As the result
our driver will have the following view::

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

Once driver class was created we need to finilize the module::

    class my_serial_driver(Module):
        def on_load(self):
            get_running_kernel().register_driver(MySerialDriver)

        def on_unload(self):
            get_running_kernel().unregister_driver(MySerialDriver)

=================
Creating a device
=================

Once the device driver has been written, we need to define device that can be
controlled by this driver. If you already have a serial device that you would
like to control, then you can skip this part. Otherwise, follow the next
instructions to create a simple serial device to test serial driver
``my_serial_driver``.

Create a simple serial device ``my_serial_device`` that will be controled by our
driver :class:`MySerialDriver`. The device class should be derived from the base
device class :class:`bb.hardware.devices.device.Device` and will have such
designator format, that our devices will have such designators:
``MY_SERIAL_DEV1``, ``MY_SERIAL_DEV2``, etc. Now we are ready::

    from bb.hardware.devices import Device
    from my_serial_driver import MySerialDriver

    class MySerialDevice(Device):
        DRIVER_CLASS=MySerialDriver
        DESIGNATOR_FORMAT="MY_SERIAL_DEV%d"

Once the device was created we can connect it with other devices from the
application.
        
============
Using driver
============

Now we can use our new serial driver :class:`MySerialDriver`. First of all
we need to load the ``my_serial_driver`` module::

    get_running_kernel().load_module("my_serial_driver")

Now we can control device and write::

    get_running_kernel().control_device("MY_SERIAL_DRIVER")




