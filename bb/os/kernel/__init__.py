#!/usr/bin/env python

"""The BB kernel.

Build-time and life-time errors.
"""

__version__ = "$Rev: 401 $"
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import signal
import traceback
import threading
import multiprocessing
import types
import re
import time

import bb
from bb.utils import caller
from bb.utils.type_check import verify_list, verify_string, verify_bool
from bb.os import OSObject, OSObjectMetadata
from bb.os.kernel.errors import *
from bb.os.kernel.schedulers import *
from bb.app import Traceable, Application
from bb.mm.mempool import MemPool, mwrite
from bb.hardware import verify_device

#_______________________________________________________________________________

# Contains kernel extensions in form: extension name, extension class.
# See kernel_extension() function to learn how to create a kernel extension.
KERNEL_EXTENSIONS_MAP = dict()

# List of extension names that have to be used by default.
# See kernel_extension() function to learn how to add an extension to kernel
# by default.
DEFAULT_KERNEL_EXTENSIONS = list()

class KernelExtension(object):
    """This class represents kernel extension."""

def kernel_extension(name, default=True):
    """This function is used as decorator and maps extension name to
    extension class."""
    verify_string(name)
    verify_bool(default)
    def catch_kernel_extension(cls):
        if not issubclass(cls, KernelExtension):
            raise TypeError("Kernel extension %s must be subclass "
                            "of KernelExtension." % cls)
        KERNEL_EXTENSIONS_MAP[name] = cls
        if default:
            DEFAULT_KERNEL_EXTENSIONS.append(name)
        return cls
    return catch_kernel_extension

#_______________________________________________________________________________

class Thread(OSObject):
    """The thread is an atomic unit action within the BB
    operating system, which describes application specific actions
    wrapped into a single context of execution.

    The following example shows how to create a new thread and add it
    to the kernel:

    class Demo(Thread):
        def __init__(self):
            Thread.__init__(self, name="DEMO")

        @Thread.runner
        def hello_world(self):
            print "Hello world!"

    thread = kernel.add_thread(Demo())

    Which is equivalent to:

    def hello_world():
        print "Hello world!"
    thread = kernel.add_thread(Thread("DEMO", hello_world))
    """

    # This constant keeps marked runners sorted by owner class. The content of
    # this variable is formed by decorator @runner.
    RUNNER_PER_CLASS = dict()

    def __init__(self, name=None, runner=None, port_name=None):
        """This constructor should always be called with keyword arguments.
        Arguments are:

        name is the thread name. This name should be unique within system
        threads. By default is None.

        target is callable object to be invoked by the start() method.
        Default is None, meaning nothing is called."""
        OSObject.__init__(self)
        self.__name = None
        if name:
            self.set_name(name)
        self.__commands = ()
        # Start working with runner initialization
        self.__runner = None
        if runner:
            self.set_runner(runner)
        else:
            self.__detect_runner_method()
        self.__port_name = None
        if port_name:
            self.set_port_name(port_name)

    @classmethod
    def runner(cls, runner):
        """Mark target method as thread's entry point."""
        # Search for the target class to which target function belongs
        runner_cls = caller(2)
        # Save the target for a nearest future when the __init__ method will
        # we called for the target_cls class.
        Thread.RUNNER_PER_CLASS[runner_cls] = runner.__name__
        return runner

    def __detect_runner_method(self):
        """Okay, let us search for the runner in methods marked with
        help of @runner decorator."""
        cls = self.__class__
        if cls.__name__ in Thread.RUNNER_PER_CLASS:
            # Since the runner here is represented by a function it will be
            # converted to a method for a given instance. Then this method
            # will be stored as attribute 'target'.
            runner_method_name = Thread.RUNNER_PER_CLASS[cls.__name__]
            runner = getattr(self, runner_method_name)
            self.set_runner(runner)

    def set_port_name(self, name):
        # TODO: check port existance.
        self.__port_name = name

    def get_port_name(self):
        return self.__port_name

    def set_name(self, name):
        """Set the given name as thread's name."""
        self.__name = verify_string(name)

    def get_name(self):
        return self.__name

    def set_runner(self, runner):
        self.__runner = runner

    def get_runner(self):
        """Returns runner. By default returns None value."""
        return self.__runner

    def get_runner_name(self):
        """Returns name of the runner which is the function name. By
        default if runner was not defined, returns None.

        def hello_world():
            print "Hello world!"

        thread = Thread("HELLO_WORLD", hello_world)
        print thread.get_runner_name()

        As result we will have string hello_world.
        """
        if self.get_runner():
            return self.get_runner().__name__
        return None

    def start(self):
        """Start the thread's activity. It arranges for the object's run()
        method."""
        self.run()

    def run(self):
        """This method represents thread's activity. You may override this
        method in a subclass. The standard run() method invokes the callable
        object passed to the object's constructor as the target argument."""
        runner = self.get_runner()
        if not runner:
            raise KernelException("Runner wasn't defined")
        runner()

    # The following methods provide support for pickle. This will allow user to
    # pickle Thread instance. Priously I was trying to use this to be able copy
    # thread instance to the file and then load it. On this moment we do not use
    # this feature. I'm still keeping it here while it's not disturb me.

    def __getstate__(self):
      corrected_dict = self.__dict__.copy() # copy the dict since we change it
      if type(corrected_dict['target']) is types.MethodType:
        del corrected_dict['target']
      return corrected_dict

    def __setstate__(self, dict_):
      self.__dict__.update(dict_)
      self.__detect_runner_method()

    def __str__(self):
        """Returns a string containing a concise, human-readable
        description of this object."""
        return "Thread %d" % self.get_name()

class Idle(Thread):
    """The special thread that runs when the system is idle."""
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE")

    @Thread.runner
    def bbos_idle_runner(self):
        pass

class Messenger(Thread):
    """This class is a special form of thread, which allows to
    automatically provide an action for received message by using
    specified map of predefined handlers.

    The following example shows the most simple case how to define a
    new message handler by using Messenger.message_handler() decorator:

    class SerialMessenger(Messenger):
        @Messenger.message_handler("SERIAL_OPEN")
        def serial_open_handler(self, message):
            print "Open serial connection"

    Or the same example, but without decorator:

    class SerialMessenger(Messenger):
        def __init__(self):
            Messenger.__init__(self)
            self.add_message_handler("SERIAL_OPEN", self.serial_open_handler)

        def serial_open_handler(self, message):
            print "Open serial connection"

    When a SerialMessenger object receives a SERIAL_OPEN message, the
    message is directed to SerialMessenger.serial_open_handler handler
    for the actual processing.

    Note, in order to privent any conflicts with already defined
    methods the message handler should be named by concatinating
    "_handler" postfix to the the name of handler,
    e.g. serial_open_handler()."""

    MESSAGE_HANDLERS_MAP_PER_CLASS = dict()
    PORT_NAME_FORMAT = "MESSENGER_PORT_%d"
    PORT_SIZE = 2
    COUNTER_PER_PORT_NAME_FORMAT = dict()

    def __init__(self, name=None, port_name=None, port_name_format=None,
                 port_size=None):
        Thread.__init__(self, name, port_name=port_name)
        # Define the format of port name or set default if required
        if not port_name_format:
            port_name_format = self.PORT_NAME_FORMAT
        if not port_name_format in self.COUNTER_PER_PORT_NAME_FORMAT:
            self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format] = 0
        # If port name was not provided it will be generated automatically by
        # using appropriate name format
        if not port_name:
            self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format] += 1
            counter = self.COUNTER_PER_PORT_NAME_FORMAT[port_name_format]
            port_name = port_name_format % counter
            if not port_size:
                port_size = self.PORT_SIZE
            get_running_kernel().add_port(Port(port_name, port_size))
        self.set_port_name(port_name)
        self.__message_handlers_map = dict()
        self.__default_message_handlers()

    def __default_message_handlers(self):
        """Set default message handlers from
        Messenger.MESSAGE_HANDLERS_BY_CLASS if such were defined."""
        cls_name = self.__class__.__name__
        if not cls_name in Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS:
            return
        message_handlers_map = \
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[cls_name]
        for command, handler in message_handlers_map.items():
            self.add_message_handler(command, handler)

    @classmethod
    def message_handler(dec_cls, cmd):
        """A special decorator to reduce a few unnecessary steps to
        add a new message handler. See add_message_handler() for more
        details."""
        verify_message_command(cmd)
        target_cls_name = caller(2)
        if not target_cls_name in table:
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[target_cls_name] = dict()
        def catch_message_handler(handler):
            Messenger.MESSAGE_HANDLERS_MAP_PER_CLASS[target_cls_name][cmd] = handler
            return handler
        return catch_message_handler

    def add_message_handler(self, command, handler):
        """Maps a command extracted from a message to the specified handler
        function."""
        if not callable(handler):
            raise Exception("The handler %s has to be callable." % handler)
        if self.has_message_handler(command):
            print "WARNING: The handler %s of the message %s will be redefined"\
                % (self.find_message_handler(command))
        self.__message_handlers_map[command] = handler

    def get_supported_messages(self):
        """Returns a list of messages for which the messenger has
        handlers."""
        return self.__message_handlers_map.keys()

    def has_message_handler(self, command):
        """This method is alias to Messenger.find_message_handler(),
        but it returns True if handler was found or False otherwise."""
        return not not self.find_message_handler(command)

    def find_message_handler(self, command):
        """Returns message handler if there is a handler for command,
        or None if there is no such handler."""
        if not command in self.get_supported_messages():
            return None
        handler = self.__message_handlers[command]
        return handler

    # TODO: create a unique runner.
    def run(self):
        """The messenger's logic."""
        message = get_running_kernel().receive_message()
        if not message:
            return
        command = message.get_command()
        handler = self.find_message_handler(command)
        if not handler:
            raise Exception("Unknown command '%s'" % command)
        handler(message)

@kernel_extension("thread_management", True)
class ThreadManagement(KernelExtension):
    def __init__(self, threads=list(), scheduler=StaticScheduler()):
        KernelExtension.__init__(self)
        print "Initialize thread management"
        self.__threads = dict()
        self.__scheduler = None
        # Select scheduler first if defined before any thread will be added
        # By default, if scheduler was not defined will be used static
        # scheduling policy.
        if scheduler:
            self.set_scheduler(scheduler)
        # Add default threads
        self.add_thread(Idle())
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
            raise KernelTypeException('Thread "%s" must be bb.os.kernel.Thread '
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
        """Add a new thread to the kernel. Return thread's object. Can be used
        as a thread factory.

        Note: this method is available in all modes, so be carefull to
        make changes."""
        if not len(args) and not len(kargs):
            raise KernelException("Nothing to process")
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
        self.echo("Add thread '%s'" % thread.get_name())
        self.__threads[ thread.get_name() ] = thread
        # Introduce thread to scheduler
        self.get_scheduler().enqueue_thread(thread)
        # Register available commands
        #self.add_commands(thread.get_commands())
        return thread

    def add_threads(self, *threads):
        """Add a list of thread to the kernel."""
        verify_list(threads)
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
            raise KernelTypeException("Scheduler '%s' must be bb.os.kernel.Scheduler "
                                  "sub-class" % scheduler)
        print "Select scheduler '%s'" % scheduler.__class__.__name__
        self.__scheduler = scheduler
        for thread in self.get_threads():
            scheduler.enqueue_thread(thread)

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

#_______________________________________________________________________________

class Message(object):
    """A message passed between threads."""
    def __init__(self, command=None, data=None, sender=None):
        self.__command = None
        self.__sender = None
        self.__data = None
        if command:
            self.set_command(command)
        self.set_sender(sender or get_running_thread().get_name())
        if data:
            self.set_data(data)
        self.__owner = self.get_sender()

    def get_owner(self):
        return self.__owner

    def set_command(self, command):
         self.__command = verify_string(command)

    def get_command(self):
        return self.__command

    def get_sender(self):
        return self.__sender

    def set_sender(self, sender):
        self.__sender = sender

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

verify_message_command = verify_string

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
        has to be represented by a string."""
        self.__name = verify_string(name)
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
            raise KernelTypeException('Message "%s" must be %s '
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
class ITC(KernelExtension):
    """Inter-Thread Communication (ITC)."""

    def __init__(self):
        KernelExtension.__init__(self)
        print "Initialize ITC"
        self.__commands = []
        self.__ports = {}

    def add_port(self, port):
        """Add a new port to the system."""
        if not isinstance(port, Port):
            raise KernelException("Port %s!")
        if self.select_port(port.get_name()):
            raise KernelException("Port '%s' has been already added"
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
            raise KernelTypeException()
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
            raise KernelTypeException("Message '%s' must be %s sub-class"
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
            raise KernelTypeException('Command "%s" must be bb.os.kernel.Command '
                                  'sub-class' % command)
        return command.get_name() in self.__commands

    def add_command(self, command):
        if self.has_command(command):
            return command
        self.__commands.append(command)
        return command

#_______________________________________________________________________________

class Driver(OSObject, OSObjectMetadata):
    """A BB device driver controls a hardware component or device
    represented by Device. Interaction with drivers is done through
    DriverManager, which can be obtained via
    Kernel.find_driver_manager().

    The following example shows the most simple case how to define a
    new action handler by using Driver.action_handler() decorator:

    class SerialDriver(Driver):
        def __init__(self):
            Driver.__init__(self, "SERIAL_DRIVER")

        @Driver.action_handler("SERIAL_OPEN")
        def open_handler(self, device):
            print "Open serial connection"

    Or the same example, but without decorator:

    class SerialDriver(Driver):
        def __init__(self):
            Driver.__init__(self, "SERIAL_DRIVER")
            self.add_action_handler("SERIAL_OPEN", self.serial_open_handler)

        def serial_open_handler(self, message):
            print "Open serial connection"

    Note, in order to privent any conflicts with already defined
    methods the action handler should be named by concatinating
    "_handler" postfix to the the name of handler,
    e.g. serial_open_handler()."""

    MESSENGER_CLASS = Messenger

    ACTION_HANDLERS_MAP_PER_CLASS = dict()

    def __init__(self, name=None, version=None):
        self.__name = None
        if name:
            self.set_name(name)
        self.__version = None
        if version:
            self.set_version(version)
        # Internal table of actions and their handlers.
        self.__action_handlers_map = dict()
        self.__default_action_handlers_map()
        self.__messenger = None
        if self.MESSENGER_CLASS:
            self.__messenger = self.MESSENGER_CLASS()

    def get_messenger(self):
        """Returns the Messenger that controls driver activity. By
        default returns None if messenger wasn't specified."""
        return self.__messenger

    def __default_action_handlers_map(self):
        """Set default action handlers from
        Driver.ACTION_HANDLERS_MAP_PER_CLASS if such were defined."""
        cls_name = self.__class__.__name__
        # Whether we have predefined action handlers
        if not cls_name in Driver.ACTION_HANDLERS_MAP_PER_CLASS:
            return
        for action, handler in Driver.ACTION_HANDLERS_MAP_PER_CLASS[cls_name].items():
            self.add_message_handler(command, handler)

    @classmethod
    def action_handler(dec_cls, action):
        """A special decorator to reduce a few unnecessary steps to
        add a new action handler. See add_action_handler() for more
        details."""
        verify_string(action)
        target_cls_name = caller(2)
        if not target_cls_name in table:
            Driver.ACTION_HANDLERS_MAP_PER_CLASS[target_cls_name] = dict()
        # Define a sepcial action catcher
        def catch_action_handler(handler):
            Driver.ACTION_HANDLERS_MAP_PER_CLASS[target_cls_name][cmd] = handler
            return handler
        # Return our catcher
        return catch_action_handler

    def add_action_handler(self, action, handler):
        """Maps an action to the associated handler function."""
        if not callable(handler):
            raise Exception("Handler must be callable.")
        if self.has_action_handler(action):
            print "WARNING: A handler '%s' is already associated with "\
                                "action '%s'" % (handler, action)
        self.__action_handlers[action] = handler

    def is_supported_action(self, action):
        """Whether appropriate handler was defined for a given
        action."""
        return action in self.get_supported_actions()

    def get_supported_actions(self):
        return self.__action_handlers_map.keys()

    def find_action_handler(self, action):
        """Returns action handler if there is a handler for action,
        or None if there is no such handler."""
        if not self.is_supported_action(action):
            return None
        handler = self.__action_handlers_map[action]
        return handler

    def attach_device(self, device):
        """Called by hardware manager to query the existence of a
        specific device and whether this driver can control it."""
        raise NotImplementedError("Please, implement this!")

    def detach_device(self, device):
        """Called by hardware manager when the device is removed in
        order to free it from driver's (system) control."""
        raise NotImplementedError("Please, implement this!")

def verify_driver(driver):
    if not isinstance(driver, Driver):
        raise Exception("Expected Driver type; received %s (is %s)" %
                        (driver, driver.__class__.__name__))

class DriverManager(object):
    """This class represents an interface to interract with Driver
    objects inside of the system.

    It is system responsibility to create and work with this
    manager. However developer may use the manager in order to define
    all device controled by particular driver."""

    def __init__(self, driver):
        self.__driver = None
        self.__devices = list()
        self.__set_driver(driver)

    def __set_driver(self, driver):
        """Private method used to select a driver that has to be managed by
        this manager."""
        verify_driver(driver)
        self.__driver = driver

    def get_driver(self):
        """Returns Driver instance."""
        return self.__driver

    def add_device(self, device):
        verify_device(device)

    def has_device(self, device):
        pass

    def get_devices(self):
        """Return a list of all devices currently bound to the driver."""
        return self.__devices

class DeviceManager(OSObject):
    """Every device in BBOS system is managed by an instance of
    this class. Device manager represents a device from the mapping.

    The following example shows how to register
    PropellerP8X32Processor from bb.hardware.processors package for
    kernel, which required from system to create DeviceManager
    instance to manage this device:

    device = PropellerP8X32Processor()
    kernel.register_device(device)
    """

    def __init__(self, device, driver=None):
        """device is a Device instance that has to be managed by this
        manager.

        driver defines a Driver instance that manages device. Please
        see Driver class."""
        OSObject.__init__(self)
        self.__device = None
        self.__set_device(device)
        self.__driver = None
        if driver:
            self.set_driver(driver)

    def __set_device(self, device):
        verify_device(device)
        self.__device = device

    def get_device(self):
        return self.__device

    def set_driver(self, driver):
        verify_driver(driver)
        self.__driver = driver

    def get_driver(self):
        """Returns Driver instance that manages this device. By default return
        None value if driver was not selected."""
        return self.__driver

    def __str__(self):
        """Returns a string containing a concise, human-readable description of
        this object."""
        return "Device manager of %s" % self.get_device().get_name()

@kernel_extension("hardware_management", True)
class HardwareManagement(KernelExtension):
    """This class provides kernel support for hardware
    management. More precisely it provides an interface for device and
    driver management and their interruction.

    The following example shows how to  :

    device = PropellerP8X32Device()
    kernel.register_device(device)
    driver = PropellerP8X32Driver()
    kernel.register_driver(driver)
    kernel.bind_device_to_driver(device, driver)
    """

    def __init__(self):
        KernelExtension.__init__(self)
        print "Initialize hardware management"
        self.__device_managers = dict()
        self.__driver_managers = dict()
        # Now use mapping to register outside devices via hardware interface
        if self.get_mapping():
            for device in mapping.hardware.get_board().get_devices():
                self.register_device(device)

    #####################
    # Device management #
    #####################

    def register_device(self, device):
        """This method registers device."""
        if self.is_registered_device(device):
            raise KernelException("Device '%s' was already registered." %
                                  device.get_name())
        self.__devices[device.get_name()] = device

    def is_registered_device(self, device):
        """Define whether or not the device was registered."""
        verify_device(device)
        return device in self.get_devices()

    def unregister_device(self, device):
        pass

    def find_device(self, name):
        """Returns the Device that is called name, or None if there is
        no such device. More precisely system is looking for DriverManager and
        then returns Driver instance, which it controls.

        This example returns a device Device of kernel named "SERIAL_DEV_0":
        device = kernel.find_device("SERIAL_DEV_0")"""
        manager = self.find_device_manager(name)
        if not manager:
            return None
        return manager.get_driver()

    def find_device_manager(self, name):
        return self.__device_managers[name]

    def get_device_managers(self):
        """Returns a list of device managers, one manager for each device."""
        return self.__device_managers.values()

    def get_devices(self):
        """Return complete list of all devices that were successfully
        registered by Kernel.register_device()."""
        devices = list()
        for manager in self.get_device_managers():
            devices.append(manager.get_device())
        return devices

    def get_unknown_devices(self):
        """Return list of unknown devices. The device is unknown when
        the system does not know the driver that can control it."""
        unknown_devices = []
        for device in self.get_devices():
            if not device.get_driver():
                unknown_devices.append(device)
        return unknown_devices

    def control_device(self, name, action, *args):
        """Device control is the most common function used for device
        control, fulfilling such tasks as accessing devices, getting
        information, sending orders, and exchanging data. This method
        calls an action for a specified device driver, causing the
        corresponding device to perform the corresponding operation.

        The device has to be register by using
        Kernel.register_device() method and then it has to be
        associated with a driver that will control this device, for
        example, this can be done by using
        Kernel.bind_device_to_driver() method.
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

    #####################
    # Driver management #
    #####################

    def register_driver(self, driver):
        """Once a driver has been registered, the DriverManager object
        will be created in order to manage driver's activity within
        the system. Thus the system does not keep Driver instance
        directly but with help of DriverManager.

        An appropriate driver manager can be obtained by passing
        driver name to Kernel.find_driver_manager() method."""
        manager = DriverManager(driver)
        self.__driver_managers[driver.NAME] = manager

    def find_driver(self, name):
        manager = self.find_driver_manager(name)
        if not manager:
            return None
        return manager.get_driver()

    def find_driver_manager(self, name):
        verify_string(name)
        return self.__driver_managers[name]

    def is_registered_driver(self, name):
        """Takes driver name and defines whether or not the driver was
        registered."""
        return not not self.find_driver_manager(name)

    def get_driver_managers(self):
        return self.__driver_managers.values()

    def get_drivers(self):
        drivers = list()
        for manager in self.get_driver_managers():
            drivers.append(manager.get_driver())
        return drivers

    def unregister_driver(self, driver):
        pass

    def bind_device_to_driver(self, device, driver):
        """Binds device to the proper driver. Driver binding is the
        process of associating a device with a device driver that can
        control it. In case when system can not bind a device to the
        proper device driver this can be done by hand with help of
        this method."""
        verify_device(device)
        if not self.is_registered_device(device):
            KernelException("In order to bind device to driver, device has to" \
                                " be registered by using register_device().")
        verify_driver(driver)
        if not self.is_registered_driver(driver):
            KernelException("In order to bind device to driver, driver has to" \
                                " be registered by using register_driver().")
        manager = self.find_driver_manager(driver)
        manager.add_device(device)
        print "Bind device '%s' to driver '%s'" % (str(device), str(driver))

    def unbind_device_from_driver(self, device, driver):
        driver.manager.remove_device(device)

#_______________________________________________________________________________

@kernel_extension("imc", False)
class IMC(KernelExtension):
    def __init__(self):
        KernelExtension.__init__(self)
        print "Initialize IMC"

#_______________________________________________________________________________

class System(OSObject, Traceable):
    """The heart of BB operating system. In order to connect with application
    inherits OSObject class."""
    def __init__(self, *args, **kargs):
        OSObject.__init__(self)
        print self.banner()
        print "Initialize kernel"
        self.__modules = {}
        # XXX: WTF?! It's very strange, but we need to do the following hack in
        # order to get __extensions attribute
        self.__extensions = getattr(self, "__extensions")
        # Initialize all kernel extensions one by one
        for extension in self.__extensions:
            extension.__init__(self)

    def get_mapping(self):
        #mapping = Application.get_running_instance().get_active_mapping()
        return None

    def echo(self, data):
        if not isinstance(data, types.StringType):
            data = str(data)
        print data

    @OSObject.simulation_method
    def test(self):
        print "Test kernel"
        if not self.get_num_threads():
            raise KernelException("At least one thread has to be added")
        # Test the system for unknown devices
        if self.get_unknown_devices():
            self.panic("Unknown devices: %s" % ", ".join([str(device) for device
                                                in self.get_unknown_devices()]))

    @OSObject.simulation_method
    def start(self):
        self.test()
        print "Start kernel"
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except KeyboardInterrupt, e:
            self.stop()
        except SystemExit, e:
            self.stop()

    @OSObject.simulation_method
    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        print "Kernel stopped"
        sys.exit(0)

    @OSObject.simulation_method
    def panic(self, text):
        """Halt the system.

        Display a message, then perform cleanups with stop. Concerning
        the application this allows to stop a single process, while
        all other processes are running."""
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        print "%s:%d:PANIC: %s" % (fname, lineno, text)
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        self.stop()

    @OSObject.simulation_method
    def banner(self):
        """Return nice BB OS banner."""
        return "BBOS Kernel v0.2.0." + \
            re.search('(\d+)', re.escape(__version__)).group(1) + ""

    # Module Management
    # This set of methods a meta-operating system specific. Such routines
    # are not supported in target embedded systems.

    def load_module(self, name):
        """Load module to the running kernel. This method connects module's
        environment and kernel's environment."""
        if name in self.__modules:
            return self.__modules[name]
        # The module wasn't loaded before. Do the import.
        self.echo("Load module '%s'" % name)
        try:
            module = __import__(name, globals(), locals(),
                                [name.rsplit('.', 1).pop()], -1)
        except ImportError, e:
            self.panic(e)
        self.__modules[name] = module
        # Start loading a new module
        on_load = getattr(module, 'on_load', None)
        if not on_load:
            self.panic("Can not load module '%s'. Method 'on_load' was not found."
                       % name)
        on_load()
        # Once the module was importer to the system it has to be removed
        # so all other kernels will be able to import this module. The
        # module instance will be saved in kernel's context.
        del sys.modules[name]
        return module

    def find_module(self, name):
        """Find module's object by its name. Return None if module was
        not identified."""
        name = verify_string(name)
        try:
            return self.__modules[name]
        except KeyError:
            return None

    def get_modules(self):
        """Return complete list of loaded modules."""
        return self.__modules.values()

    def unload_module(self, name):
        raise NotImplemented

def get_running_kernel():
    """Just another useful wrapper. Return the currently running kernel
    object."""
    # XXX On this moment if no kernels are running, the None value will
    # be returned. Maybe we need to make an exception?
    return Traceable.find_running_instance(Kernel)

def Kernel(**selected_extensions):
    """This kernel factory creates and returns Kernel class with all
    required extensions. selected_extensions contains extensions that
    have to be included (if they have True value) or excluded (if they
    have False value) from list of extensions that will extend kernel
    functionality."""
    use_extensions = DEFAULT_KERNEL_EXTENSIONS
    # Verify and update the list of extensions to be used
    for extension, is_required in selected_extensions.items():
        if extension not in KERNEL_EXTENSIONS_MAP:
            raise Exception("Unknown kernel extension: %s" % extension)
        if not is_required and extension in use_extensions:
            use_extensions.remove(extension)
        elif is_required and extension not in use_extensions:
            use_extensions.append(extension)
    # If IMC extension wasn't selected but the mapping with this kernel
    # interructs with other mappings (sends or receives any data) through an
    # application network, this extension will be added by force.
    app = Application.get_active_instance()
    if 'imc' not in use_extensions and \
            len(app.network.edges([app.get_active_mapping()])):
        use_extensions.append('imc')
    # Translate a list of required extensions to the list of classes that
    # represent these extensions
    extensions = tuple([KERNEL_EXTENSIONS_MAP[extension] for extension in
                        use_extensions])
    kernel_cls = type("Kernel", (System, ) + extensions,
                  {'__extensions': extensions})
    return kernel_cls()
