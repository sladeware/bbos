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
from bb.app import Object, Traceable
from module import caller

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

class KernelError(Exception):
    """The root error."""

class KernelTypeError(Exception):
    """Type error."""

class KernelModuleError(KernelError):
    """Unable to load an expected module."""

DEFAULT_COMMANDS = ['BBOS_DRIVER_OPEN', 'BBOS_DRIVER_CLOSE']

class Message:
    """A message passed between threads."""
    def __init__(self, command, data=None, sender=None):
        self.set_command(command)
        self.set_sender(sender or get_running_thread().get_name())
        self.set_data(data)

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

class Thread(object):
    """The thread is an atomic unit if action within the BBOS operating system,
    which describes application specific actions wrapped into a single context
    of execution."""

    name = None
    target = None
    commands = []

    __marked_runners = {}

    def __init__(self, name=None, target=None):
        self.__messages = []
        if name:
            self.set_name(name)
        elif hasattr(self, 'name'):
            self.set_name(self.name)
        if target:
            self.target = target
        else:
            # Okay, let us search for the runner in methods marked with help
            # of @runner decorator.
            klass = self.__class__
            if klass.__name__ in self.__marked_runners:
                # Since the runner here is represented by a function it will be
                # converted to a method for a given instance. Then this method
                # will be stored as attribute target.
                runner = self.__marked_runners[klass.__name__]
                setattr(self, runner.__name__, types.MethodType(runner, self))
                self.target = getattr(self, runner.__name__)

    def is_supported_command(self, command):
        return command in self.commands

    def get_commands(self):
        """Return a tuple of commands that module supports for 
        communication purposes."""
        return self.commands

    def get_name(self):
        return self.name

    def get_runner_name(self):
        if self.target:
            return self.target.__name__

    def set_name(self, name):
        self.name = verify_string(name)

    def start(self):
        if self.target:
            return self.target()

    @classmethod
    def runner(klass, target):
        """Mark target method as thread's entry point."""
        # Search for the target_klass to which target function belongs.
        target_klass = inspect.getouterframes(inspect.currentframe())[1][3]
        # Save the target for a nearest future when the __init__ method will
        # we called for the target_klass class.
        klass.__marked_runners[target_klass] = target
        return target

    # Inter-Thread Communication

    def put_message(self, message):
        if not isinstance(message, Message):
            raise KernelTypeError('Message "%s" must be bb.os.kernel.Message '
                                  'sub-class' % message)
        self.__messages.append(message)

    def get_message(self):
        if self.has_message():
            return self.__messages.pop(0)
        return None

    def has_message(self):
        return not not len(self.__messages)

class Idle(Thread):
    """The special thread that runs when the system is idle."""
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE")

    @Thread.runner
    def bbos_idle_runner(self):
        pass

class Scheduler:
    """Provides the algorithms to select the threads for execution. 
    Base scheduler class."""

    def __init__(self, *arg_list, **arg_dict):
        pass

    def move(self):
        """Decide who to run now."""
        raise NotImplemented

    def get_running_thread(self):
        raise NotImplemented

    def enqueue_thread(self, thread):
        raise NotImplemented

    def dequeue_thread(self, thread):
        raise NotImplemented

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
        self.__modules = {}
        self.init(*args, **kargs)

    # System Management

    @Object.sim_method
    def printer(self, data):
        if not isinstance(data, types.StringType):
            data = str(data)
        prefix = ''
        if multiprocessing.current_process().pid: # see application number of processes
            prefix = "[%d] " % multiprocessing.current_process().pid
        print prefix + data

    def init(self, threads=[], commands=[], scheduler=None):
        self.printer(self.banner())
        self.printer("Initialize kernel")
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

    @Object.sim_method
    def test(self):
        if not self.get_number_of_threads():
            raise KernelError("At least one thread has to be added")

    @Object.sim_method
    def start(self):
        self.test()
        self.printer("Start kernel")
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    @Object.sim_method
    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        self.printer("Kernel stopped")

    @Object.sim_method
    def panic(self, text):
        """Halt the system.
        Display a message, then perform cleanups with stop. Concerning the
        application this allows to stop a single process, while all other
        processes are running."""
        self.printer("PANIC: %s" % text)
        # XXX we do not call stop() method here to do no stop the system twice.
        # exit() function will raise SystemExit exception, which will actually
        # call kernel's stop. See start() method for more information.
        exit()

    @Object.sim_method
    def banner(self):
        return "BBOS Kernel v0.2.0." + \
            re.search('(\d+)', re.escape(__version__)).group(1) + ""

    # Thread Management

    def find_thread(self, thread):
        if type(thread) is types.StringType:
            if thread in self.__threads:
                return self.__threads[thread]
        elif isinstance(thread, Thread):
            if thread.get_name() in self.__threads:
                return thread
        else:
            raise KernelTypeError('Thread "%s" must be bb.os.kernel.Thread '
                                  'sub-class' % thread)
        return None

    def has_thread(self, thread):
        """Test for presence of thread in the kernel's list of threads."""
        return not self.find_thread(thread) is None

    def remove_thread(self, thread):
        raise NotImplemented()

    def add_thread(self, *args, **kargs):
        """Add a new thread to the kernel. Return thread's object.
        Note: this method is available in all modes, so be carefull to
        make changes."""
        if not len(args) and not len(kargs):
            raise NotImplemented()
        thread = self.find_thread(args[0])
        if thread:
            raise Exception("Thread '%s' has been already added" % thread.get_name())
        if type(args[0]) is types.StringType:
            thread = Thread(*args)
        else:
            thread = args[0]
        self.printer("Add thread '%s'" % thread.get_name())
        self.__threads[ thread.get_name() ] = thread
        # Introduce thread to scheduler
        if self.has_scheduler():
            self.get_scheduler().enqueue_thread(thread)
        # Register available commands
        self.add_commands(thread.get_commands())
        return thread

    def add_threads(self, *threads):
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
            raise KernelTypeError('Scheduler "%s" must be bb.os.kernel.Scheduler '
                                  'sub-class' % scheduler)
        self.printer("Select scheduler '%s'" % scheduler.__class__.__name__)
        self.__scheduler = scheduler
        for thread in self.get_threads():
            scheduler.enqueue_thread(thread)

    def get_scheduler(self):
        return self.__scheduler

    def has_scheduler(self):
        return not self.get_scheduler() is None

    def switch_thread(self):
        thread = self.find_thread(self.get_scheduler().get_running_thread())
        thread.start()

    # Inter-Thread Communication (ITC)

    def send_message(self, receiver, message):
        if not isinstance(message, Message):
            raise KernelTypeError('Message "%s" must be bb.os.kernel.Message '
                                  'sub-class' % message)
        thread = self.find_thread(receiver)
        if not thread:
            self.panic("Receiver '%s' can not be found" % receiver)
        # Define the sender
        if not message.get_sender():
            message.set_sender(get_running_thread().get_name())
        # In order to privent an errors with unknown commands, if the thread
        # has predefined list of commands that have to be
        # used in order to communicate with it, we will try to find the command
        # from message in this list
        if thread.get_commands() and \
                not message.get_command() in thread.get_commands():
            print thread.get_commands()
            raise KernelError("Thread '%s' does not support the command '%s'" %
                              (receiver, message.get_command()))
        thread.put_message(message)

    def receive_message(self, receiver=None):
        if not receiver:
            thread = self.get_scheduler().get_running_thread()
        else:
            thread = self.find_thread(receiver)
        if not thread:
            raise KernelError("Receiver '%s' can not be found" % receiver)
        return thread.get_message()

    # Commands

    def get_number_of_commands(self):
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

    def load_module(self, name, alias=None):
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
            self.printer("Load module '%s' as '%s'" % (name, alias))
        else:
            self.printer("Load module '%s'" % name)
        #fake_name = name + str(id(self))
        #if fake_name in sys.modules:
        #    raise Exception("Fixed name is not unique")
        try:
            module = Importer.load(name, globals(), locals(),
                                   [name.rsplit('.', 1).pop()])
        except ImportError, e:
            self.panic(e)
        self.__modules[alias or name] = module
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
        self.printer("Register driver '%s'" % driver.get_name())
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
