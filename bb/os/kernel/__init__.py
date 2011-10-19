#!/usr/bin/env python

__version__ = "$Rev: 401 $"
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import traceback
import threading
import multiprocessing
import types
import re
import inspect

import bb
from bb.utils.type_check import verify_list, verify_string
from bb.os import OSObjectMetadata
from bb.os.hardware import Driver, Device
from bb.os.kernel.schedulers import *
from bb.app import Object, Traceable, Application

class KernelError(Exception):
    """The root error."""

class KernelTypeError(KernelError):
    """Type error."""

class KernelModuleError(KernelError):
    """Unable to load an expected module."""

def get_running_kernel():
    """Just another useful wrapper. Return the currently running kernel
    object."""
    # XXX On this moment if no kernels are running, the None value will
    # be returned. Maybe we need to make an exception?
    return Traceable.find_running_instance(Kernel)

def get_running_thread():
    """Return currently running thread object."""
    kernel = get_running_kernel()
    if kernel.has_scheduler():
        return kernel.get_scheduler().get_running_thread()
    else:
        raise NotImplemented()

class Message(object):
    """A message passed between threads."""
    def __init__(self, command=None, data=None, sender=None):
        self.__command = None
        self.__sender = None
        self.__data = None
        if command:
            self.set_command(command)
        self.set_sender(sender or get_running_thread().get_name())
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

class Thread(Object):
    """The thread is an atomic unit if action within the BBOS operating system,
    which describes application specific actions wrapped into a single context
    of execution."""

    name = None
    target = None
    commands = ()

    marked_runners = {}

    def __init__(self, name=None, target=None, port_name=None):
        """This constructor should always be called with keyword arguments.
        Arguments are:

        name is the thread name. This name should be unique within system
        threads. By default is None.

        target is callable object to be invoked by the start() method.
        Default is None, meaning nothing is called."""
        Object.__init__(self)
        # Select thread name
        if name:
            self.set_name(name)
        elif hasattr(self, "name"):
            self.set_name(self.name)
        # Start working with runner initialization
        self.__runner_method_name = None
        if target:
            self.set_runner(target)
        else:
            self.__detect_runner_method()
        self.__port_name = None
        self.set_port_name(port_name)

    def set_port_name(self, name):
        self.__port_name = name

    def get_port_name(self):
        return self.__port_name

    def __detect_runner_method(self):
        """Okay, let us search for the runner in methods marked with help
        of @runner decorator."""
        klass = self.__class__
        if klass.__name__ in self.marked_runners:
            # Since the runner here is represented by a function it will be
            # converted to a method for a given instance. Then this method
            # will be stored as attribute 'target'.
            if not self.__runner_method_name:
                self.__runner_method_name = self.marked_runners[klass.__name__]
            target = getattr(self, self.__runner_method_name)
            self.set_runner(target)

    def is_supported_command(self, command):
        return command in self.commands

    def get_commands(self):
        """Return a tuple of commands that module supports for communication
        purposes."""
        return self.commands

    def set_name(self, name):
        self.name = verify_string(name)

    def get_name(self):
        return self.name

    def set_runner(self, target):
        self.target = target

    def get_runner(self):
        return self.target

    def get_runner_name(self):
        if self.get_runner():
            return self.get_runner().__name__

    def start(self):
        """Start the thread's activity. It arranges for the object's run()
        method."""
        self.run()

    def run(self):
        """This method represents thread's activity. You may override this
        method in a subclass. The standard run() method invokes the callable
        object passed to the object's constructor as the target argument"""
        target = self.get_runner()
        if not target:
            raise KernelError("Runner wasn't defined")
        target()

    @classmethod
    def runner(klass, target):
        """Mark target method as thread's entry point."""
        # Search for the target_klass to which target function belongs.
        target_klass = inspect.getouterframes(inspect.currentframe())[1][3]
        # Save the target for a nearest future when the __init__ method will
        # we called for the target_klass class.
        klass.marked_runners[target_klass] = target.__name__
        return target

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

class Messenger(Thread):
    """This class is a special form of thread, which allows to automatically
    provide an action for received command by using specified table of
    predefined command handlers."""

    def __init__(self, name=None, port_name=None, command_handlers_table=None):
        Thread.__init__(self, name, port_name=port_name)
        self.__command_handlers_table = command_handlers_table

    def get_commands(self):
        return self.__command_handlers_table.keys()

    def get_command_handlers(self):
        return self.__command_handlers_table.values()

    def get_command_handlers_table(self):
        return self.__command_handlers_table

    def add_command_handler(self, command, handler):
        self.__command_handlers_table[command] = handler

    def has_commmand_handler(self, command):
        return not not self.find_command_handler(command)

    def find_command_handler(self, command):
        if not command in self.get_commands():
            raise Exception("A handler for '%s' command was not specified"
                % command)
        handler = self.__command_handlers_table[command]
        if not handler:
            raise Exception("Messenger doesn't support '%s' command" % command)
        return handler

    def run(self):
        message = get_running_kernel().receive_message()
        if not message:
            return
        command = message.get_command()
        if not command in self.get_commands():
            raise Exception("Unknown command '%s'" % command)
        handler = self.find_command_handler(command)
        handler(message)

class Manager(object):
    all_command_handlers = dict()

    def __init__(self, name=None, port_name=None):
        self.name = name
        klass = self.__class__.__name__
        if not klass in self.all_command_handlers:
            raise KernelError("%s manager doesn't have any command or handler"
                              % klass)
        self.__command_handlers = dict()
        for command, handler in self.all_command_handlers[klass].items():
            handler = getattr(self, handler.__name__, None)
            self.__command_handlers[command] = handler
        self.__messenger = Messenger(self.name, port_name=port_name,
                                     command_handlers_table=self.__command_handlers)
        get_running_kernel().add_thread(self.__messenger)

    @classmethod
    def command_handler(klass, command):
        verify_string(command)
        # Search for the target_klass to which handler belongs
        target_klass = inspect.getouterframes(inspect.currentframe())[1][3]
        if not target_klass in Manager.all_command_handlers:
            Manager.all_command_handlers[target_klass] = dict()
        def handle(handler):
            Manager.all_command_handlers[target_klass][command] = handler
            return handler
        return handle

class Port(object):
    """Protected messaging pool for communication between threads."""

    def __init__(self, name, capacity):
        assert capacity > 0, "Port capacity must be greater than zero"
        self.__messages = []
        # Initialize messaging pool
        from bb.mm.mempool import MemPool
        self.__mp = MemPool(capacity, 12)
        # Initialize port name
        self.__name = None
        self.set_name(name)

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
        from bb.mm.mempool import mwrite
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
            raise KernelTypeError('Message "%s" must be %s '
                                  'sub-class' % (message, Message))
        self.__messages.append(message)

    def fetch_message(self):
        """Shift and return top message from a queue if port has any message."""
        if self.count_messages():
            return self.__messages.pop(0)
        return None

    def count_messages(self):
        return len(self.__messages)

class Idle(Thread):
    """The special thread that runs when the system is idle."""
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE")

    @Thread.runner
    def bbos_idle_runner(self):
        pass

class Kernel(Object, Traceable):
    """The heart of BB operating system. In order to connect with application
    inherits Object class."""
    def __init__(self, *args, **kargs):
        Object.__init__(self)
        self.__threads = {}
        self.__drivers = []
        self.__devices = []
        self.__commands = []
        self.__scheduler = None
        self.__ports = {}
        self.__modules = {}
        self.init(*args, **kargs)

    # System Management

    def init(self, threads=[], commands=[], scheduler=StaticScheduler()):
        """By default, if scheduler was not defined will be used static
        scheduling policy."""
        self.echo(self.banner())
        self.echo("Initialize kernel")
        # Select scheduler first if defined before any thread will be added
        if scheduler:
            self.set_scheduler(scheduler)
        # Add default threads
        self.add_thread(Idle())
        # Add additional user threads
        if len(threads):
            self.add_threads(threads)
        if len(commands):
            self.add_commands(commands)
        # Now we will with mapping to define outside devices or hardware that
        # we need to revive
        mapping = Application.get_running_instance().get_active_mapping()
        # Detect and initialize board
        board = mapping.hardware.get_board()
        self.echo("'%s' board detected" % board.get_name())
        if board.driver:
            pass
        # Detect and initialize processor
        processor = mapping.hardware.get_processor()
        self.echo("'%s' processor detected" % processor.get_name())
        if processor.driver:
            self.load_module(mapping.hardware.get_processor().driver)

    def echo(self, data):
        if not isinstance(data, types.StringType):
            data = str(data)
        prefix = ''
        # See number of processes within an application. Do not show process 
        # identifier if we have less than two processes.
        if Application.get_running_instance().get_num_processes() > 1:
            mapping = Application.get_running_instance().get_active_mapping()
            prefix = "[%s] " % mapping.name
        print prefix + data

    @Object.simulation_method
    def test(self):
        if not self.get_number_of_threads():
            raise KernelError("At least one thread has to be added")

    @Object.simulation_method
    def start(self):
        self.test()
        self.echo("Start kernel")
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except KeyboardInterrupt, e:
            self.stop()
        except SystemExit, e:
            self.stop()

    @Object.simulation_method
    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        self.echo("Kernel stopped")
        sys.exit(1)

    @Object.simulation_method
    def panic(self, text):
        """Halt the system.

        Display a message, then perform cleanups with stop. Concerning the
        application this allows to stop a single process, while all other
        processes are running."""
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        self.echo("%s:%d:PANIC: %s" % (fname, lineno, text))
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        self.stop()

    @Object.simulation_method
    def banner(self):
        """Return nice BB OS banner."""
        return "BBOS Kernel v0.2.0." + \
            re.search('(\d+)', re.escape(__version__)).group(1) + ""

    # Thread Management

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
            raise KernelTypeError('Thread "%s" must be bb.os.kernel.Thread '
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
            raise KernelError("Nothing to process")
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
        self.add_commands(thread.get_commands())
        return thread

    def add_threads(self, *threads):
        """Add a list of thread to the kernel."""
        verify_list(threads)
        for thread in threads:
            self.add_thread(thread)

    def get_threads(self):
        return self.__threads.values()

    def get_number_of_threads(self):
        return len(self.get_threads())

    # Thread Scheduling

    def set_scheduler(self, scheduler):
        """Select scheduler."""
        if not isinstance(scheduler, Scheduler):
            raise KernelTypeError("Scheduler '%s' must be bb.os.kernel.Scheduler "
                                  "sub-class" % scheduler)
        self.echo("Select scheduler '%s'" % scheduler.__class__.__name__)
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

    # Inter-Thread Communication (ITC)

    def add_port(self, port):
        if not isinstance(port, Port):
            raise KernelError("Port %s!")
        if self.select_port(port.get_name()):
            raise Exception("Port '%s' has been already added"
                            % port.get_name())
        self.echo("Add port '%s'" % port.get_name())
        self.__ports[port.get_name()] = port
        return port

    def remove_port(self, port):
        raise NotImplemented()

    def select_port(self, name):
        """Select port by name and return its instance. The name must be
        represented by a string. If port can not be selected, return None."""
        if not type(name) is types.StringType:
            raise KernelTypeError()
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
            raise KernelTypeError("Message '%s' must be %s sub-class"
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
            raise KernelTypeError('Command "%s" must be bb.os.kernel.Command '
                                  'sub-class' % command)
        return command.get_name() in self.__commands

    def add_command(self, command):
        if self.has_command(command):
            return command
        self.__commands.append(command)
        return command

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

    # Device Management

    def control_device(self, name, action, *args):
        device = self.find_device_by_name(name)
        if not device:
            self.panic("Cannot found device '%s'" % name)
        driver = device.driver
        f = getattr(driver, action)
        return f(*args)

    def register_device(self, device):
        self.echo("Register device '%s'" % device.name)
        self.__devices.append(device)

    def find_device_by_name(self, name):
        for device in self.get_devices():
            if device.name == name:
                return device

    def get_devices(self):
        return self.__devices

    # Driver Management

    def register_driver(self, driver_class):
        if not type(driver_class) is types.TypeType:
            raise KernelTypeError("Not a class")
        if not issubclass(driver_class, Driver):
            raise KernelTypeError("Not a subclass of Driver: %s" % driver)
        # Now we can create driver instance that will be in use
        driver = driver_class()
        self.echo("Register driver '%s' version '%s'"
            % (driver.get_name(), str(driver.get_version())) )
        self.__drivers.append(driver)
        driver.init()
        return driver

    def get_drivers(self):
        """Return complete list of registered drivers."""
        return self.__drivers

    def find_driver_by_name(self, name):
        for driver in self.get_drivers():
            if driver.get_name() == name:
                return driver
        return None

    def get_num_drivers(self):
        return len(self.get_drivers())

    def select_last_driver(self):
        return self.find_driver_by_index(self.get_num_drivers() - 1)

    def find_driver_by_index(self, index):
        return self.get_drivers()[index]

    def unregister_driver(self, driver):
        driver.exit()

