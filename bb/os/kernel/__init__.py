#!/usr/bin/env python

__version__ = "$Rev$"
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import traceback
import threading
import multiprocessing
import types
import imp
import collections
import re
import inspect

import bb
from bb.utils.type_check import verify_list, verify_string
from bb.utils.importer import Importer
from bb.os.kernel.schedulers import *
from bb.app import Object, Traceable, Context

def get_running_kernel():
    """Just another useful wrapper. Return the currently running kernel
    object."""
    # XXX On this moment if no kernels are running, the None value will
    # be returned. Maybe we need to make an exception?
    return Traceable.find_running_instance(Kernel)

def printk(data):
    if not isinstance(data, types.StringType):
        data = str(data)
    prefix = ''
    # see number of processes within an application
    if multiprocessing.current_process().pid:
        prefix = "[%d] " % multiprocessing.current_process().pid
    print prefix + data

def get_running_thread():
    """Return currently running thread object."""
    kernel = get_running_kernel()
    if kernel.has_scheduler():
        return kernel.get_scheduler().get_running_thread()
    else:
        raise NotImplemented()

class KernelError(Exception):
    """The root error."""

class KernelTypeError(Exception):
    """Type error."""

class KernelModuleError(KernelError):
    """Unable to load an expected module."""

DEFAULT_COMMANDS = ['BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE']

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

def _patch(self):
  key = object.__getattribute__(self, '_ThreadLocal__key')
  d = threading.current_thread().__dict__.get(key)
  if d is None:
    d = {}
    threading.current_thread().__dict__[key] = d
    object.__setattr__(self, '__dict__', d)
    class_ = type(self)
    if class_.__init__ is not object.__init__:
      args, kargs = object.__getattribute__(self, '_ThreadLocal__args')
      class_.__init__(self, *args, **kargs)
  else:
    object.__setattr__(self, '__dict__', d)

class _ThreadLocalBase(object):
  def __new__(class_, *args, **kargs):
    self = object.__new__(class_)
    key = '_LocalThread__key', 'thread.local.' + str(id(self))
    object.__setattr__(self, '_ThreadLocal__key', key)
    object.__setattr__(self, '_ThreadLocal__args', (args, kargs))
    object.__setattr__(self, '_ThreadLocal__lock', threading.RLock())
    if (args or kargs) and (class_.__init__ is object.__init__):
      raise TypeError()
    dict = object.__getattribute__(self, '__dict__')
    threading.current_thread().__dict__[key] = dict
    return self

class ThreadLocal(_ThreadLocalBase):
  __slots__ = '_ThreadLocal__key', '_ThreadLocal__args', '_ThreadLocal__lock'

  def __getattribute__(self, name):
    lock = object.__getattribute__(self, '_ThreadLocal__lock')
    lock.acquire()
    try:
      _patch(self)
      return object.__getattribute__(self, name)
    finally:
      lock.release()

  def __setattr__(self, name, value):
    if name == '__dict__':
      raise AttributeError("%r object attribute '__dict__' is read-only"
        % self.__class__.__name__)
    lock = object.__getattribute__(self, '_ThreadLocal__lock')
    lock.acquire()
    try:
      _patch(self)
      return object.__setattr__(self, name, value)
    finally:
      lock.release()

  def setdefault(self, key, value):
      self.__dict__.setdefault(key, value)

class Thread(Object):
    """The thread is an atomic unit if action within the BBOS operating system,
    which describes application specific actions wrapped into a single context
    of execution."""

    name = None
    target = None
    commands = ()
    local_class = ThreadLocal

    marked_runners = {}

    def __init__(self, name=None, target=None, port_id=None):
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
        # Create instance to keep local data
        if not self.local_class:
          raise NotImplemented
        self.__local = self.local_class()
        self.__port_id = None
        self.set_port_id(port_id)

    def set_port_id(self, port):
        self.__port = port

    def get_port_id(self):
        return self.__port

    def get_local(self):
      return self.__local

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
        target = self.get_runner()
        if target:
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
            return self.__messages.pop(index)
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

class Driver(Thread):
    pass

class Kernel(Object, Traceable):
    """The heart of BB operating system. In order to connect with application
    inherits Object class."""
    def __init__(self, *args, **kargs):
        Object.__init__(self)
        self.__threads = {}
        self.__drivers = {}
        self.__commands = []
        self.__scheduler = None
        self.__ports = {}
        self.__modules = {}
        self.init(*args, **kargs)

    # System Management

    def init(self, threads=[], commands=[], scheduler=StaticScheduler()):
        """By default, if scheduler was not defined will be used static
        scheduling policy."""
        printk(self.banner())
        printk("Initialize kernel")
        # Select scheduler first if defined before any thread will be added
        if scheduler:
            self.set_scheduler(scheduler)
        self.add_commands(DEFAULT_COMMANDS)
        # Add default threads
        self.add_thread(Idle())
        # Add additional user threads
        if len(threads):
            self.add_threads(threads)
        if len(commands):
            self.add_commands(commands)

    @Object.simulation_method
    def test(self):
        if not self.get_number_of_threads():
            raise KernelError("At least one thread has to be added")

    @Object.simulation_method
    def start(self):
        self.test()
        printk("Start kernel")
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    @Object.simulation_method
    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        printk("Kernel stopped")

    @Object.simulation_method
    def panic(self, text):
        """Halt the system.

        Display a message, then perform cleanups with stop. Concerning the
        application this allows to stop a single process, while all other
        processes are running."""
        lineno = inspect.getouterframes(inspect.currentframe())[2][2]
        fname = inspect.getmodule(inspect.stack()[2][0]).__file__
        printk("%s:%d:PANIC: %s" % (fname, lineno, text))
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        exit()

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
        printk("Add thread '%s'" % thread.get_name())
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
        printk("Select scheduler '%s'" % scheduler.__class__.__name__)
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

    def add_port(self, *args, **kargs):
        if not len(args) and not len(kargs):
            raise KernelError("Nothing to process")
        if len(args) == 1 and isinstance(args[0], Port):
            port = self.select_port(args[0])
            if port:
                raise Exception("Port '%s' has been already added"
                                % port.get_name())
        else:
            port = Port(*args, **kargs)
        printk("Add port '%s'" % port.get_name())
        self.__ports[port.get_name()] = port
        return port

    def remove_port(self, port):
        raise NotImplemented()

    def select_port(self, port):
        """Select port return its instance. The port value can be represented
        by a string or Port object. If port can not be selected, return None."""
        if type(port) is types.StringType:
            if port in self.__ports:
                return self.__ports[port]
        return None

    def alloc_message(self, command=None, data=None):
        """Allocate a new message from a port and return Message instance."""
        sender = get_running_thread()
        if not sender.get_port_id():
            self.panic("Cannot allocate a memory for a message to be sent. "
                       "Sender '%s' doesn't have a port for communication." %
                       sender.get_name())
        port = self.select_port( sender.get_port_id() )
        if not port:
            self.panic("Kernel does not support port '%s'" % port)
        # Eventually allocate a new message from the port and return it back
        message = port.alloc_message(command, data)
        return message

    def free_message(self, message):
        """Free memory used by the message."""
        owner = message.get_owner()
        if not owner:
            owner = get_running_thread().get_port_id()
        port = self.select_port(owner)
        if not port:
            self.panic("Message %s can not be free. "
                       "It seems like field owner was broken."
                       % message)
        port.free_message(message)

    def is_inactive_message(self, message):
        return get_running_kernel().get_port_id() == message.get_owner()

    def send_message(self, receiver, message):
        """Send a message to receiver from sender."""
        if not isinstance(message, Message):
            raise KernelTypeError("Message '%s' must be %s sub-class"
                                  % (message, Message))
        receiver = get_running_kernel().select_thread(receiver)
        if not receiver.get_port_id():
            self.panic("Cannot send a message."
                       "Receiver '%s' doesn't have a port for communication." %
                       receiver.get_name())
        port = self.select_port(receiver.get_port_id())
        if not port:
            self.panic("Kernel does not support port '%s' that is used by "
                       "receiver '%s'"
                       % (port.get_name(), receiver.get_name()))
        port.push_message(message)

    def receive_message(self):
        receiver = get_running_thread()
        if not receiver.get_port_id():
            self.panic("Cannot receive a message."
                       "Receiver '%s' doesn't have a port for communication." %
                       receiver.get_name())
        port = self.select_port(receiver.get_port_id())
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

    def load_module(self, name, args=None, alias=None):
        """Load module to the running kernel. This method allows to avoid
        built-in __import__ function and connect module's environment and
        kernel's environment. If alias is defined the module will be registred
        by this name. This helps to sort out the problem with long module
        names."""
        if name in self.__modules:
            if alias:
                self.__modules[alias] = self.__modules[name]
                del self.__modules[name]
            return self.__modules[name]
        elif alias in self.__modules:
            return self.__modules[alias]
        # The module wasn't loaded before. Do the import.
        if alias:
            printk("Load module '%s' as '%s'" % (name, alias))
        else:
            printk("Load module '%s'" % name)
        try:
            module = Importer.load(name, globals(), locals(),
                                   [name.rsplit('.', 1).pop()])
        except ImportError, e:
            self.panic(e)
        self.__modules[alias or name] = module
        # Bootstrap
        bootstrap = getattr(module, 'bootstrap', None)
        if not bootstrap:
            self.panic("%s doesn't have bootstrap" % name)
        bootstrap(args)
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

    # Driver Management

    def register_driver(self, driver):
        if not isinstance(driver, Driver):
            raise KernelTypeError("Not a Driver: %s" % driver)
        printk("Register driver '%s'" % driver.get_name())
        self.__drivers[driver.get_name()] = driver
        self.add_thread(driver)

    def get_drivers(self):
        """Return complete list of registered drivers."""
        return self.__drivers.values()

    def find_driver(self, name):
        raise NotImplemented

    def unregister_driver(self, driver):
        raise NotImplemented

import bb.os.kernel.setup
