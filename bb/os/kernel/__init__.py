#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A kernel represents a non-blocking computational resource, which is in most
cases simply a core of a microcontroller. Threads run within a kernel using a
customizable time sharing scheduler algorithm.

The kernel is represented by :class:`bb.os.kernel.Kernel` class and consists of
extensions. The extension can be created with help of :func:`kernel_extension`
decorator.
"""

__version__ = "$Rev: 401 $"
__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "<oleks.sviridenko@gmail.com> Oleksandr Sviridenko"

import sys
import signal
import traceback
import threading
import multiprocessing
import types
import re
import inspect
import time

import bb
from bb.utils.builtins import caller
from bb.utils import type_check
from bb.os.kernel import errors
from bb.os.kernel.schedulers import *
from bb.app import appmanager
from bb.app.application import Traceable, Application
from bb.mm.mempool import MemPool, mwrite
from bb.hardware import verify_device, Device
from bb.builder.toolchains import propgcc
from bb.builder.toolchains import simulator

class OS(object):
    """This class describes BB operating system.

    The :class:`Mapping` uses this class to create :class:`OS` instance. Once
    operating system is created, the mapping will call :func:`OS.main` entry
    point and then :func:`OS.start` to run the system.
    """

    class Object(Application.Object):
        """The root main class for BBOS kernel and other operating system
        parts.
        """
        def __init__(self):
            Application.Object.__init__(self)

        class Metadata(object):
            NAME = None

            def __init__(self, name=None):
                self.__name = None
                if name:
                    self.set_name(name)
                elif hasattr(self, "NAME"):
                    self.set_name(self.NAME)

            def set_name(self, name):
                self.__name = name

            def get_name(self):
                return self.__name

    def __init__(self, **kargs):
        self.kernel = kernel_factory()
        threads = kargs.get('threads', None)
        if threads:
            self.kernel.add_threads(threads)

@simulator.SimulationToolchain.pack(OS)
class OSSimulation(simulator.SimulationToolchain.Package):
    FILES = ("__init__sim.py",)

@propgcc.PropGCCToolchain.pack(OS)
class OSPackage(propgcc.PropGCCToolchain.Package):
    FILES = ("../kernel.c",)

    def on_unpack(self):
        propgcc.PropGCCToolchain.Package.on_unpack(self)
        os_class = self.get_object()
        os = os_class()
        # Add threads and create unique output file name
        threads = os.kernel.get_threads()
        for thread in threads:
            self.get_toolchain().add_source(thread)
        output_filename = '_'.join([t.__class__.__name__ for t in threads])
        self.get_toolchain().compiler.set_output_filename(output_filename)

class Kernel(OS.Object, Traceable):
    """The heart of BB operating system. In order to connect with application
    inherits OS.Object class.
    """

    class Extension(object):
        """This is base class for kernel extensions."""
        pass

    def __init__(self, *args, **kargs):
        OS.Object.__init__(self)
        print "Building microkernel..."
        # XXX: WTF?! It's very strange, but we need to do the following hack in
        # order to get __extensions attribute
        self.__extensions = getattr(self, "__extensions")
        # Initialize all kernel extensions one by one
        for extension in self.__extensions:
            print "* init extension '%s'" % extension.__name__
            extension.__init__(self)

# Contains kernel extensions in form: extension name, extension class.
# See kernel_extension() function to learn how to create a kernel extension.
_KERNEL_EXTENSIONS = dict()

# List of extensions that have to be used by default.
# See kernel_extension() function to learn how to add an extension to this list.
_DEFAULT_KERNEL_EXTENSIONS = list()

def kernel_extension(name, default=True):
    """This function is used as decorator and maps extension's name to
    extension's class. The extension can be also marked as `default` and thus
    be used by default.
    """
    type_check.verify_string(name)
    type_check.verify_bool(default)
    def catch_kernel_extension(cls):
        if not issubclass(cls, Kernel.Extension):
            raise TypeError("Kernel extension %s must be subclass "
                            "of Kernel.Extension." % cls)
        _KERNEL_EXTENSIONS[name] = cls
        if default:
            _DEFAULT_KERNEL_EXTENSIONS.append(name)
        return cls
    return catch_kernel_extension

@kernel_extension("module_management", True)
class ModuleManagement(Kernel.Extension):
    """This kernel extension aims to control module management."""

    def __init__(self):
        self.__modules = dict()

    def load_module(self, path, args=None):
        """Load module `path` to the running kernel and pass arguments `args` to
        its initialization method.
        """
        if path in self.__modules:
            return self.__modules[path]
        # The module wasn't loaded before. Do the import.
        self.echo("Loading module '%s'" % path)
        name = path.rsplit('.', 1).pop()
        try:
            py_module = __import__(path, globals(), locals(), [name], -1)
        except ImportError, e:
            self.panic(e)
        # Start loading a new module
        klass = getattr(py_module, name, None)
        if not klass or not issubclass(klass, Module):
            self.panic("Cannot load '%s'. '%s' control module class can not be found." %
                       (path, name))
        bb_module = klass(args)
        bb_module.on_load()
        # Register module and call on_load method
        self.__modules[path] = bb_module
        # XXX: do we need to remove py_module? The the comment below.
        # Once the module was importer to the system it has to be removed
        # so all other kernels will be able to import this module. The
        # module instance will be saved in kernel's context.
        del sys.modules[path]
        return bb_module

    def find_module(self, name):
        """Find module's object by its name. Return None if module was
        not identified.
        """
        name = type_check.verify_string(name)
        try:
            return self.__modules[name]
        except KeyError:
            return None

    def get_modules(self):
        """Return complete list of loaded modules."""
        return self.__modules.values()

    def unload_module(self, name):
        """Unload module `name`."""
        raise NotImplemented

class Module(object):
    """Module is meta-operating system specific object that aims to extend
    kernel functionallity.
    """

    def __init__(self, args=None):
        self.args = args

    def on_load(self):
        """Abstract method. This method is called by kernel once module is
        loaded.
        """
        pass

    def on_unload(self):
        """Abstract method. This method is called by kernel when module has
        to be unloaded.
        """
        pass

class Thread(OS.Object):
    RUNNER = None

    def __init__(self, name=None, runner=None):
        OS.Object.__init__(self)
        self.__name = None
        if runner:
            self.set_runner(runner)
        elif hasattr(self, "RUNNER"):
            self.__runner = self.RUNNER
        if name:
            self.set_name(name)
        elif hasattr(self, "NAME"):
            self.set_name(getattr(self, "NAME"))

    def get_runner(self):
        return self.__runner

    def set_name(self, name):
        """Set the given name as thread's name."""
        self.__name = type_check.verify_string(name)

    def get_name(self):
        return self.__name

@kernel_extension("thread_management", True)
class ThreadManagement(Kernel.Extension):
    """This class represents thread management that is used as kernel
    extension."""

    Thread=Thread

    def __init__(self, threads=list(), scheduler=StaticScheduler()):
        Kernel.Extension.__init__(self)
        self.__threads = dict()
        self.__scheduler = None
        # Select scheduler first if defined before any thread will be added
        # By default, if scheduler was not defined will be used static
        # scheduling policy.
        if scheduler:
            self.set_scheduler(scheduler)
        # Add additional user threads
        if len(threads):
            self.add_threads(threads)

    def select_thread(self, thread):
        """Select thread from the set of added thread. thread can be provided in
        a few ways. If thread is represented by a string, then a thread with
        such name will be searched and its object returned. If thread is
        represented by Thread instance and such thread belongs to this kernel,
        the same object will be returned. Otherwise return None."""
        # String
        if type(thread) is types.StringType:
            if thread in self.__threads:
                return self.__threads[thread]
        # Thread instance
        elif isinstance(thread, Thread):
            if thread.get_name() in self.__threads:
                return thread
        else:
            raise errors.KernelTypeException('Thread "%s" must be bb.os.kernel.Thread '
                                  'sub-class' % thread)
        return None

    def has_thread(self, thread):
        """Test for presence of thread in the kernel's list of threads. Return
        True if the kernel owns this thread, or False otherwise.

        Note: this method simply uses select_thread()."""
        return not self.select_thread(thread) is None

    def remove_thread(self, thread):
        raise NotImplemented()

    def add_thread(self, *args, **kargs):
        if not len(args) and not len(kargs):
            raise Kernel.Exception("Nothing to process")
        if len(args) == 1:
            thread = self.select_thread(args[0])
            if thread:
                raise Exception("Thread '%s' has been already added"
                                % thread.get_name())
        if type(args[0]) is types.StringType:
            # Create a new thread instance
            thread = Thread(*args)
        else:
            thread = args[0]
        self.__threads[ thread.get_name() ] = thread
        return thread

    def add_threads(self, threads):
        """Add a list of thread to the kernel."""
        type_check.verify_list(threads)
        for thread in threads:
            self.add_thread(thread)

    def get_threads(self):
        return self.__threads.values()

    def get_num_threads(self):
        return len(self.get_threads())

    # Thread Scheduling

    def set_scheduler(self, scheduler):
        """Select scheduler."""
        if not isinstance(scheduler, Scheduler):
            raise errors.KernelTypeException("Scheduler '%s' must be bb.os.kernel.Scheduler "
                                  "sub-class" % scheduler)
        print "* select scheduler '%s'" % scheduler.__class__.__name__
        self.__scheduler = scheduler
        #for thread in self.get_threads():
        #    scheduler.enqueue_thread(thread)

    def get_scheduler(self):
        return self.__scheduler

    def has_scheduler(self):
        return not self.get_scheduler() is None

    def switch_thread(self):
        thread = self.select_thread(self.get_scheduler().get_running_thread())
        thread.start()

def get_running_thread():
    """Return currently running thread object."""
    kernel = get_running_kernel()
    if kernel.has_scheduler():
        return kernel.get_scheduler().get_running_thread()
    else:
        raise NotImplemented()

class Port(object):
    """Protected messaging pool for communication between threads."""

    def __init__(self, name, capacity):
        assert capacity > 0, "Port capacity must be greater than zero"
        self.__messages = []
        self.__mp = MemPool(capacity, 12)
        self.__name = None
        self.set_name(name)

    def get_capacity(self):
        return self.__mp.get_num_chunks()

    def set_name(self, name):
        """Set a new name to the port and return this name back. The name
        has to be represented by a string.
        """
        self.__name = type_check.verify_string(name)
        return name

    def get_name(self):
        """Return port name (string)."""
        return self.__name

    def alloc_message(self, command=None, data=None, sender=None):
        if not sender:
            sender = self.get_name()
        message = self.__mp.malloc()
        if not message:
            return None
        mwrite(message, Message(command, data, sender))
        return message

    def free_message(self, message):
        """Free memory related to message from the appropriate memory pool."""
        self.__mp.free(message)

    def push_message(self, message):
        if not isinstance(message, Message):
            raise errors.KernelTypeException('Message "%s" must be %s '
                                  'sub-class' % (message, Message))
        self.__messages.append(message)

    def fetch_message(self):
        """Shift and return top message from a queue if port has any message."""
        if self.count_messages():
            return self.__messages.pop(0)
        return None

    def count_messages(self):
        return len(self.__messages)

@kernel_extension("itc", True)
class ITC(Kernel.Extension):
    """Inter-Thread Communication (ITC)."""

    def __init__(self):
        Kernel.Extension.__init__(self)
        self.__commands = []
        self.__ports = {}

    def add_port(self, port):
        """Add a new port to the system."""
        if not isinstance(port, Port):
            raise Kernel.Exception("Port %s!")
        if self.select_port(port.get_name()):
            raise Kernel.Exception("Port '%s' has been already added"
                              % port.get_name())
        print "Add port '%s' of %d messages" % (port.get_name(), port.get_capacity())
        self.__ports[port.get_name()] = port
        return port

    def remove_port(self, port):
        raise NotImplemented()

    def select_port(self, name):
        """Select port by name and return its instance. The name must be
        represented by a string. If port can not be selected, return None."""
        if not type(name) is types.StringType:
            raise errors.KernelTypeException()
        if name in self.__ports:
            return self.__ports[name]
        return None

    def alloc_message(self, command=None, data=None):
        """Allocate a new message from a port and return Message instance."""
        sender = get_running_thread()
        if not sender.get_port_name():
            self.panic("Cannot allocate a memory for a message to be sent. "
                       "Sender '%s' doesn't have a port for communication." %
                       sender.get_name())
        port = self.select_port( sender.get_port_name() )
        if not port:
            self.panic("Kernel does not support port '%s'" % port)
        # Eventually allocate a new message from the port and return it back
        message = port.alloc_message(command, data)
        return message

    def free_message(self, message):
        """Free memory used by the message."""
        owner = message.get_owner()
        if not owner:
            owner = get_running_thread().get_port_name()
        port = self.select_port(owner)
        if not port:
            self.panic("Message %s can not be free. "
                       "It seems like field owner was broken."
                       % message)
        port.free_message(message)

    def send_message(self, name, message):
        """Send a message to receiver from sender."""
        if not isinstance(message, Message):
            raise errors.KernelTypeException("Message '%s' must be %s sub-class"
                                  % (message, Message))
        #receiver = self.select_thread(name)
        #if not receiver:
        #    self.panic("Cannot found thread-receiver '%s'" % name)
        #if not receiver.get_port_name():
        #    self.panic("Cannot send a message."
        #               "Receiver '%s' doesn't have a port for communication." %
        #               receiver.get_name())
        #port = self.select_port(receiver.get_port_name())
        port = self.select_port(name)
        if not port:
            self.panic("Kernel does not support port '%s' that is used by "
                       "receiver '%s'"
                       % (port.get_name(), receiver.get_name()))
        port.push_message(message)

    def receive_message(self):
        receiver = get_running_thread()
        if not receiver.get_port_name():
            self.panic("Cannot receive a message. "
                       "Receiver '%s' doesn't have a port for communication."
                        % receiver.get_name())
        port = self.select_port(receiver.get_port_name())
        if not port:
            self.panic("Kernel does not support port '%s' that is used by "
                       "receiver '%s'"
                       % (port.get_name(), receiver.get_name()))
        return port.fetch_message()

    # Commands

    def get_num_commands(self):
        return len(self.get_commands())

    def get_commands(self):
        """Return complete list of commands that was presented to the system."""
        return self.__commands

    def get_command(self, command):
        if not self.has_command(command):
            return None
        if type(command) is types.StringType:
            return self.__commands[command]
        elif type(command) is types.InstanceType:
            return self.__commands[ command.get_name() ]

    def add_commands(self, commands):
        for command in commands:
            self.add_command(command)

    def has_command(self, command):
        if type(command) is types.StringType:
            return command in self.__commands
        if type(command) != types.TypeType or not issubclass(command, Command):
            raise errors.KernelTypeException('Command "%s" must be bb.os.kernel.Command '
                                  'sub-class' % command)
        return command.get_name() in self.__commands

    def add_command(self, command):
        if self.has_command(command):
            return command
        self.__commands.append(command)
        return command

@kernel_extension("hardware_management", True)
class HardwareManagement(Kernel.Extension):
    """This class represents kernel extension that provides hardware
    management. More precisely it provides an interface for device and
    driver management and their interruction.

    The following example shows how to create device and driver that will
    control it, and bind them::

        from bb.os.drivers.propeller_p8x32 import PropellerP8X32Driver
        driver = PropellerP8X32Driver()
        kernel.register_driver(driver)

        from bb.hardware.devices.processors.propeller_p8x32 import PropellerP8X32A
        device = PropellerP8X32A()
        kernel.register_device(device)

        kernel.bind_device_to_driver(device, driver)
    """

    def __init__(self):
        Kernel.Extension.__init__(self)
        self.__device_managers = dict()
        self.__driver_managers = dict()
        # Now use mapping to register outside devices via hardware interface
        #mapping = self.get_mapping()
        # XXX: do we need to warn user that this kernel is outside of mapping?
        #if mapping:
        #    core = mapping.hardware.get_core()
        #    print "\tCore: %s" % core
        #    processor = mapping.hardware.get_processor()
        #    print "\tProcessor: %s" % processor
        #    board = mapping.hardware.get_board()
        #    print "\tBoard: %s" % board
        #    if board:
        #        for device in board.find_elements(Device):
        #            self.register_device(device)

    def register_device(self, device):
        """This method registers device. For each new device will be created
        :class:`DeviceManager` instance that will control it. Device is
        registering by its designator
        (see :func:`bb.hardware.primitives.primitive.Primitive.get_designator`).

        The system will also try to identify driver that will helps to control
        this device. Once the driver was found, it will be registered with help
        of :func:`register_driver` and the device will be bind to it by using
        :func:`bind_device_to_driver`.
        """
        if self.is_registered_device(device):
            raise Kernel.Exception("Device '%s' was already registered." %
                                   device.get_designator())
        manager = DeviceManager(device)
        self.__device_managers[device.get_designator()] = manager

    def is_registered_device(self, device):
        """Define whether or not the device was registered."""
        verify_device(device)
        return device in self.get_devices()

    def unregister_device(self, device):
        pass

    def find_device(self, name):
        """Return :class:`bb.hardware.devices.device.Device` that is called
        `name`, or ``None`` if there is
        no such device. More precisely system is looking for
        :class:`DeviceManager` by using :func:`find_device_manager` and then
        returns :class:`bb.hardware.devices.device.Device` instance, which it
        controls.

        This example returns a device of kernel named ``SERIAL_DEV_0``::

            device = kernel.find_device("SERIAL_DEV_0")
        """
        manager = self.find_device_manager(name)
        if not manager:
            return None
        return manager.get_driver()

    def find_device_manager(self, name):
        """Return :class:`DeviceManager` by `name`."""
        if name not in self.__device_managers:
            raise Exception("Device manager that controls device %s wasn't found" %
                            name)
        return self.__device_managers[name]

    def get_device_managers(self):
        """Returns a list of device managers, one manager for each device."""
        return self.__device_managers.values()

    def get_devices(self):
        """Return complete list of all devices that were successfully
        registered by :func:`register_device` method.
        """
        devices = list()
        for manager in self.get_device_managers():
            devices.append(manager.get_device())
        return devices

    def get_unknown_devices(self):
        """Return list of unknown devices. The device is called unknown when
        the system does not know the driver that can control it.
        """
        unknown_devices = []
        for manager in self.get_device_managers():
            if not manager.get_driver():
                unknown_devices.append(manager.get_device())
        return unknown_devices

    def control_device(self, name, action, *args):
        """Device control is the most common function used for device control,
        fulfilling such tasks as accessing devices, getting information, sending
        orders, and exchanging data. This method calls an action for a specified
        device driver, causing the corresponding device to perform the
        corresponding operation.

        The device has to be register by using :func:`register_device` method
        and then it has to be associated with a driver that will control this
        device. For example, this can be done by using
        :func:`bind_device_to_driver` method.
        """
        # Try to find target device
        device = self.find_device(name)
        if not device:
            self.panic("Cannot found device '%s'" % name)
        driver = device.get_driver()
        if not driver:
            self.panic("No drivers associated with %s device" % name)
        f = getattr(driver, action)
        return f(device, *args)

    def register_driver(self, driver):
        """Register driver so it can be used to control devices.

        Once a driver has been registered, the :class:`DriverManager` object
        will be created in order to manage driver's activity within the
        system. Thus the system does not keep :class:`Driver` instance directly
        but with help of :class:`DriverManager`.

        An appropriate driver manager can be obtained by passing driver name to
        :func:`find_driver_manager` method.
        """
        manager = DriverManager(driver)
        self.__driver_managers[driver.NAME] = manager

    def find_driver(self, name):
        manager = self.find_driver_manager(name)
        if not manager:
            return None
        return manager.get_driver()

    def find_driver_manager(self, name):
        """Find driver manager."""
        type_check.verify_string(name)
        return self.__driver_managers[name]

    def is_registered_driver(self, name):
        """Takes driver `name` and defines whether or not the driver was
        registered.
        """
        return not not self.find_driver_manager(name)

    def get_driver_managers(self):
        """Return list of all driver managers."""
        return self.__driver_managers.values()

    def get_drivers(self):
        """Retunr list of all registered drivers."""
        drivers = list()
        for manager in self.get_driver_managers():
            drivers.append(manager.get_driver())
        return drivers

    def unregister_driver(self, driver):
        pass

    def bind_device_to_driver(self, device, driver):
        """Bind :class:`bb.hardware.devices.device.Device` to the proper
        :class:`Driver`. Driver binding is the process of associating a device
        with a device driver that can control it. In case when system can not
        bind a device to the proper device driver this can be done by hand with
        help of this method.

        As an opptosite method to unbind device from driver see
        :func:`unbind_device_from_driver`.
        """
        verify_device(device)
        if not self.is_registered_device(device):
            Kernel.Exception("In order to bind device to driver, device has to" \
                                 " be registered by using register_device().")
        verify_driver(driver)
        if not self.is_registered_driver(driver):
            Kernel.Exception("In order to bind device to driver, driver has to" \
                                 " be registered by using register_driver().")
        manager = self.find_driver_manager(driver)
        manager.add_device(device)
        print "Bind device '%s' to driver '%s'" % (str(device), str(driver))

    def unbind_device_from_driver(self, device, driver):
        """Unbind :class:`bb.hardware.devices.device.Device` from the
        :class:`Driver`."""
        driver.manager.remove_device(device)

@kernel_extension("imc", False)
class IMC(Kernel.Extension):
    def __init__(self):
        Kernel.Extension.__init__(self)

def kernel_factory(**selected_extensions):
    """This kernel factory creates and returns :class:`Kernel` based class with
    all required extensions. `selected_extensions` contains extensions that have
    to be included (if they have ``True`` value) or excluded (if they have
    ``False`` value) from list of extensions that will extend kernel
    functionality.
    """
    use_extensions = _DEFAULT_KERNEL_EXTENSIONS
    # Verify and update the list of extensions to be used
    for extension, is_required in selected_extensions.items():
        if extension not in _KERNEL_EXTENSIONS:
            raise Exception("Unknown kernel extension: %s" % extension)
        if not is_required and extension in use_extensions:
            use_extensions.remove(extension)
        elif is_required and extension not in use_extensions:
            use_extensions.append(extension)
    # If IMC extension wasn't selected but the mapping with this kernel
    # interructs with other mappings (sends or receives any data) through an
    # application network, this extension will be added by force.
    app = appmanager.get_running_application()
    # TODO(todo): resolve the problem and uncomment it
    #if 'imc' not in use_extensions and \
    #        len(app.network.edges([app.get_active_mapping()])):
    #    use_extensions.append('imc')
    # Translate a list of required extensions to the list of classes that
    # represent these extensions
    extensions = tuple([_KERNEL_EXTENSIONS[extension] for extension in
                        use_extensions])
    kernel_cls = type("Kernel", (Kernel, ) + extensions,
                  {'__extensions': extensions})
    return kernel_cls()
