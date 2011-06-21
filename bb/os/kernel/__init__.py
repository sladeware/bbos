#!/usr/bin/env python

"""BBOS kernel."""

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import sys
import traceback
from types import *

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
        if type(other) is StringType:
            return self.get_name() == other
        elif (type(other) is InstanceType and isinstance(other, Command)) \
                or (type(other) is ClassType and issubclass(other, Command)): 
            return self.get_name() == other.get_name()

    @classmethod
    def get_doc(cls):
        return cls.__doc__

#______________________________________________________________________________

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
        if not isinstance(command, Command):
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

    def put_message(self, message):
        if not isinstance(message, Message):
            raise KernelTypeError('Message "%s" must be bb.os.kernel.Message '
                                  'sub-class' % message)
        self.messages.append(message)

    def get_message(self):
        if self.has_messages():
            return self.messages.pop(0)
        return None

    def start(self):
        self.run()

    def run(self):
        if self.target:
            return self.target()

    @classmethod
    def runner(cls, target):
        cls.target = target
        return target

#______________________________________________________________________________

def idle_runner():
    return

class Idle(Thread):
    def __init__(self):
        Thread.__init__(self, "BBOS_IDLE", idle_runner)

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

#______________________________________________________________________________

class Module(Thread):
    pass

#______________________________________________________________________________

from bb.os.hardware import Hardware

class Kernel:
    def __init__(self, threads=[], commands=[]):
        print self.banner()
        print "Initialize kernel"
        self.__hardware = Hardware()
        self.__threads = {}
        self.__commands = {}
        self.__scheduler = None
        self.__modules = {}
        self.add_commands(DEFAULT_COMMANDS)
        if len(threads):
            self.add_threads(threads)
        if len(commands):
            self.add_commands(commands)

    def banner(self):
        return "BBOS Kernel v"

    # Hardware Management

    def get_hardware(self):
        return self.__hardware

    # Thread Management

    def get_thread(self, thread):
        """Test for presence of thread and return thread's object. Return 
        None if kernel does have such thread."""
        if type(thread) is StringType:
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
        """Add a new thread to the kernel."""
        if not len(arg_list):
            raise NotImplemented()
        thread = self.get_thread(arg_list[0])
        if thread:
            raise KernelError("Thread '%s' has been already added" % thread.get_name())
        if type(arg_list[0]) is StringType:
            thread = Thread(*arg_list)
        else:
            thread = arg_list[0]
        print "Add thread '%s'" % thread.get_name()
        self.__threads[ thread.get_name() ] = thread
        if self.get_scheduler():
            self.__scheduler.enqueue(thread)
        return thread

    def add_threads(self, threads):
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
        if type(command) == StringType:
            return self.__commands[command]
        elif type(command) == InstanceType:
            return self.__commands[ command.get_name() ]

    def add_commands(self, commands):
        for command in commands:
            self.add_command(command)

    def has_command(self, command):
        if type(command) == StringType:
            return command in self.__commands
        if type(command) != TypeType or not issubclass(command, Command):
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
        try:
            __import__(mod_path)
        except ImportError:
            traceback.print_exc(file=sys.stderr)
            raise KernelModuleError
        mod = sys.modules[mod_path]
        mod_class_name = mod.__name__.split(".").pop()
        try:
            mod_class = getattr(mod, mod_class_name)
        except AttributeError:
            raise KernelModuleError("Module '%s' should have class '%s'" % 
                                    mod_path, mod_class_name)
        mod_inst = mod_class()
        self.__modules[mod_path] = mod_inst
        return mod_inst

    def get_modules(self):
        return self.__modules.values()

    def get_module(self, mod_path):
        raise NotImplemented

    def remove_module(self, mod_path):
        raise NotImplemented

    # System Management

    def test(self):
        if not self.get_number_of_threads():
            raise NoThreads("At least one thread has to be added")

    def start(self):
        self.test()
        print "Start kernel"
        try:
            if self.has_scheduler():
                while True:
                    self.get_scheduler().move()
                    self.switch_thread()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Shutdown everything and perform a clean system stop."""
        print "Kernel stoped."

    def panic(self, text):
        """Halt the system. Display a message, then perform cleanups with exit."""
        print "Panic: %s" % text
        exit()

