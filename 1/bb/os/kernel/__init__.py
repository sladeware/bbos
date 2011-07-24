#!/usr/bin/env python

"""The BBOS kernel API""" 

__version__ = "$Rev$"
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import traceback
import threading
import types
import os.path

from bb.apps.utils.type_verification import verify_list
from bb.os.object import Object
from bb import app

running_kernels = {}

def get_running_kernel():
    tid = threading.current_thread().ident
    if not tid in running_kernels:
        return None
    return running_kernels[tid]

def importer(mod_path):
    """Replacement for built-in __import__ primitive. importer allows to import modules 
    as in the standard fashion importer('os.path'), and also as importer('os/path') 
    or even os.importer('os/path.py')."""
    # The module path is a directory or file. Provide dot-separator.
    if os.path.isfile(mod_path) or os.path.isdir(mod_path):
        head = mod_path
        mod_path = ''
        while head:
            head, tail = os.path.split(head)
            if not len(mod_path):
                mod_path = tail
            else:
                mod_path = '.'.join([tail, mod_path])
    try:
        __import__(mod_path)
    except ImportError:
        traceback.print_exc(file=sys.stderr)
        raise KernelModuleError("Cannot import module %s" % mod_path)
    mod = sys.modules[mod_path]
    mod_class_name = mod.__name__.split('.').pop()
    try:
        mod_class = getattr(mod, mod_class_name)
    except AttributeError:
        raise KernelModuleError("Module '%s' should have control class '%s'" % 
                                mod_path, mod_class_name)
    mod_inst = mod_class()
    return mod_inst

#______________________________________________________________________________
# Kernel exceptions

class KernelError(Exception):
    """The root error."""

class KernelTypeError(Exception):
    """Type error."""

class KernelModuleError(KernelError):
    """Unable to load an expected module."""

#______________________________________________________________________________

class Command(object):
    def __repr__(self):
        return self.get_name()

    @classmethod
    def get_name(cls):
        return cls.__name__

    def __eq__(self, other):
        if type(other) is types.StringType:
            return self.get_name() == other
        elif (type(other) is types.InstanceType and isinstance(other, Command)) \
                or (type(other) is types.ClassType and issubclass(other, Command)): 
            return self.get_name() == other.get_name()

    @classmethod
    def get_doc(cls):
        return cls.__doc__

class BBOS_DRIVER_OPEN(Command):
    """Driver Command to open target device."""

class BBOS_DRIVER_CLOSE(Command):
    """Driver command to close target device."""

DEFAULT_COMMANDS = [BBOS_DRIVER_OPEN, BBOS_DRIVER_CLOSE]

#______________________________________________________________________________

class Message:
    """A message passed between threads."""
    def __init__(self, sender, command, data):
        self.set_command(command)
        self.set_sender(sender)
        self.set_data(data)

    def set_command(self, command):
        if not issubclass(command, Command): # not isinstance
            raise KernelTypeError('Command "%s" must be bb.os.kernel.Command '
                                  'sub-class.' % command)
        self.__command = command

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

#______________________________________________________________________________

class Thread:
    name = None
    target = None

    def __init__(self, name=None, target=None):
        self.messages = []
        if name:
            self.name = name
        if target:
            self.target = target

    def get_name(self):
        return self.name

    def get_runner_name(self):
        if self.target:
            return self.target.__name__
        else:
            return self.run.__name__

    def set_name(self, name):
        self.name = name

    def start(self):
        self.run()

    def run(self):
        if self.target:
            return self.target()

    @classmethod
    def runner(cls, target):
        cls.target = target
        return target

		# Inter-Thread Communication

    def put_message(self, message):
        if not isinstance(message, Message):
            raise KernelTypeError('Message "%s" must be bb.os.kernel.Message '
                                  'sub-class' % message)
        self.messages.append(message)

    def get_message(self):
        if self.has_messages():
            return self.messages.pop(0)
        return None

    def has_messages(self):
        return not not len(self.messages)

#______________________________________________________________________________

def bbos_idle_runner():
    return

class Idle(Thread):
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE", bbos_idle_runner)

#______________________________________________________________________________

class Scheduler:
    """Provides the algorithms to select the threads for execution. 
    Base scheduler class."""

    def __init__(self, *arg_list, **arg_dict):
        pass

    def move(self):
        """Decide who to run now."""
        raise NotImplemented

    def myself(self):
        raise NotImplemented

    def enqueue(self, thread):
        raise NotImplemented

    def dequeue(self, thread):
        raise NotImplemented

class Module(Thread):
    """A loadable kernel module is an object that contains functionality to 
    extend the BBOS kernel. Such functionality can be represented by an 
    application or hardware device driver. Since we are not always able to 
    provide an appropriate mechanism for the target operating system, the goal 
    of the module is to create a complete view of the system in simulation mode, 
    which will be used by BBB as a model is built."""
    commands=()

    def __init__(self, *arg_list, **arg_dict):
        Thread.__init__(self, *arg_list, **arg_dict)

    def find_command(self, command_name):
        """Find an appropriate module class for a command command_name."""
        for command in self.commands:
            if command.get_name() == command_name:
                return command

    def get_commands(self):
        """Return a tuple of commands that module supports for 
        communication purposes."""
        return self.commands

class Kernel(Object):
    def __init__(self, *arg_list, **arg_dict):
        Object.__init__(self)
        self.__hardware = Hardware()
        self.__threads = {}
        self.__commands = {}
        self.__scheduler = None
        self.__modules = {}
        # Start initialization (simulation only)
        self.init(*arg_list, **arg_dict)

    @Object.sim_method
    def printk(self, message):
        print message

    # System Management

    @Object.sim_method
    def init(self, threads=[], commands=[]):
        print self.banner()
        print "Initialize kernel"
        self.add_commands(DEFAULT_COMMANDS)
        if len(threads):
            self.add_threads(threads)
        if len(commands):
            self.add_commands(commands)

    def get_status(self):
        return self.__status

    @Object.sim_method
    def test(self):
        if not self.get_number_of_threads():
            raise KernelError("At least one thread has to be added")

    @Object.sim_method
    def start(self):
        tid = threading.current_thread().ident
        running_kernels[tid] = self
        self.test()
        print "Start kernel"
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except KeyboardInterrupt:
            self.stop()

    @Object.sim_method
    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        print "Kernel stoped."

    @Object.sim_method
    def panic(self, text):
        """Halt the system. Display a message, then perform cleanups with exit."""
        print "Panic: %s" % text
        exit()

    @Object.sim_method
    def banner(self):
        return "BBOS Kernel vALPHA"

    # Hardware Management

    def get_hardware(self):
        return self.__hardware

    # Thread Management

    def get_thread(self, thread):
        """Test for presence of thread and return thread's object. Return 
        None if kernel does have such thread."""
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
        return not self.get_thread(thread) is None

    def remove_thread(self, thread):
        raise NotImplemented()

    def add_thread(self, *arg_list):
        """Add a new thread to the kernel. This method is available in all modes, so be
        carefull to make changes."""
        if not len(arg_list):
            raise NotImplemented()
        thread = self.get_thread(arg_list[0])
        if thread:
            raise KernelError("Thread '%s' has been already added" % thread.get_name())
        if type(arg_list[0]) is types.StringType:
            thread = Thread(*arg_list)
        else:
            thread = arg_list[0]
        self.printk("Add thread '%s'" % thread.get_name())
        self.__threads[ thread.get_name() ] = thread
        if self.get_scheduler():
            self.__scheduler.enqueue(thread)
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
        if not isinstance(scheduler, Scheduler):
            raise KernelTypeError('Scheduler "%s" must be bb.os.kernel.Scheduler '
                                  'sub-class' % scheduler)
        self.__scheduler = scheduler
        self.add_thread(Idle())

    def get_scheduler(self):
        return self.__scheduler

    def has_scheduler(self):
        return not self.get_scheduler() is None

    def switch_thread(self):
        thread = self.get_thread(self.get_scheduler().get_next_thread())
        thread.start()

    # Inter-Thread Communication (ITC)

    def send_message(self, receiver, message):
        if not isinstance(message, Message):
            raise KernelTypeError('Message "%s" must be bb.os.kernel.Message '
                                  'sub-class' % message)
        receiver = self.get_thread(receiver)
        receiver.put_message(message)

    def receive_message(self, receiver=None):
        if not receiver:
            if not self.has_scheduler():
                raise KernelError("No scheduler")
            receiver = self.scheduler.get_next_thread()
        receiver = self.get_thread(receiver)
        return receiver.get_message()

    # Commands

    def get_number_of_commands(self):
        return len(self.get_commands())

    def get_commands(self):
        return self.__commands.values()

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
            raise KernelError("Command '%s' has been already added" % 
                              command.get_name())
        self.__commands[ command.get_name() ] = command
        return command

    # Module Management

    def add_module(self, mod_path):
        """Load and register module by using importer"""
        mod_inst = importer(mod_path)
        self.__modules[mod_path] = mod_inst
        # If module is recognised as a driver
        if isinstance(mod_inst, Driver):
            self.get_hardware().add_driver(mod_inst)
        self.add_thread(mod_inst)
        return mod_inst

    def get_modules(self):
        return self.__modules.values()

    def get_module(self, mod_path):
        raise NotImplemented

    def remove_module(self, mod_path):
        raise NotImplemented

#______________________________________________________________________________

from bb.os.hardware import Core, Driver

class Hardware:
    """This class represents interface between kernel and hardware abstraction.
    """
    def __init__(self):
        self.__core = None
        self.__drivers = {}

    # Board Management

    def get_board(self):
        return self.get_processor().get_owner()

    # Processor Management

    def get_processor(self):
        return self.__core.get_owner()

    # Core Management

    def set_core(self, core):
        if not isinstance(core, Core):
            raise TypeError('Core must be bb.os.hardware.Core sub-class')
        self.__core = core

    def get_core(self):
        return self.__core

    # Driver Management

    def add_driver(self, driver):
        if not isinstance(driver, Driver):
            raise TypeError('%s must be bb.os.hardware.Driver sub-class' % driver)
        self.__drivers[ driver.get_name() ] = driver

    def has_driver(self, *arg_list):
        if type(arg_list[0]) is types.StringType:
            return not self.find_driver(arg_list[0]) is None
        elif isinstance(arg_list[0], Driver):
            return not self.find_driver(arg_list[0].get_name()) is None

    def find_driver(self, name):
        if not type(name) is types.StringType:
            raise TypeError("Driver name must be a string")
        if name in self.__drivers:
            return self.__drivers[name]
        return None

    def remove_driver(self, *arg_list):
        raise NotImplemented()

import bb.os.kernel.setup

