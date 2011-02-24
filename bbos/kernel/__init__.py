
__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import os
import sys
from types import *

from bbos.kernel.thread import Thread
from bbos.kernel.message import Message
from bbos.kernel.idle import Idle
from bbos.config import Configurable

_default_messages = ["BBOS_DRIVER_INIT", "BBOS_DRIVER_OPEN", "BBOS_DRIVER_CLOSE"]

class Kernel(Configurable):
    def __init__(self, threads=[], messages=[]):
        self.threads = {}
        self.messages = {}
        self.sched = None
        self.modules = {}
        self.add_messages(_default_messages)
        if len(threads):
            self.add_threads(threads)
        if len(messages):
            self.add_messages(messages)

    def _config(self, proj):
        '''Generate the source code for the bbos.h header file used to late bind BBOS
        processes, threads and etc just before building. We need this since the
        C macro language is seriously underpowered for our purposes.'''
        try:
            f = open("bbos.h", "w")
        except IOError:
            print "There were problems writing to %s" % "bbos.h"
            traceback.print_exc(file=sys.stderr)
            raise
        f.write("/*\n"
                " * This is BBOS generated source code used for late binding application\n"
                " * features just before compile time.\n"
                " *\n"
                " * Please do not edit this by hand, as your changes will be lost.\n"
                " *\n"
                " * %s\n"
                " */\n"
                "#ifndef __BBOS_H\n"
                "#define __BBOS_H\n"
                "\n"  % (__copyright__))
        print "Process %d thread(s)" % self.get_number_of_threads()
        f.write("/* Threads */\n")
        f.write("#define BBOS_NUMBER_OF_THREADS (%d)\n" % self.get_number_of_threads())
        next_id = 0
        for thread in self.threads.values():
            print "%20s : %4d" % (thread.get_name(), next_id)
            f.write("#define %s (%s)\n" % (thread.get_name(), next_id))
            next_id += 1
        print "Process %d message(s)" % self.get_number_of_messages()
        f.write("/* Messages */\n")
        f.write("#define BBOS_NUMBER_OF_MESSAGES (%d)\n" % self.get_number_of_messages())
        next_id = 0
        for message in self.messages.values():
            print "%20s : %4d" % (message.get_name(), next_id)
            f.write("#define %s (%s)\n" % (message.get_name(), next_id))
            next_id += 1
        if self.get_scheduler():
            print "Scheduler has been enabled"
            f.write("/* Scheduling */\n")
            f.write("#define BBOS_SCHED_ENABLED\n")
        f.write("#endif /* __BBOS_H */\n")
        # Compile
        proj.add_sources([os.path.join(os.environ['BBOSHOME'], 'bbos/kernel.c'),
                          os.path.join(os.environ['BBOSHOME'], 'bbos/port.c'),
                          os.path.join(os.environ['BBOSHOME'], 'bbos/thread.c')])
        proj.add_include_dirs(['.', os.path.join(os.environ['BBOSHOME'], 'bbos')])

    def get_number_of_threads(self):
        return len(self.get_threads())

    def get_number_of_messages(self):
        return len(self.get_messages())
        
    def set_scheduler(self, sched):
        self.sched = sched
        self.add_thread(Idle())

    def get_scheduler(self):
        return self.sched

    def has_message(self, message):
        if type(message) == StringType:
            return self.messages.has_key(message)
        elif type(message) == InstanceType:
            if not isinstance(message, Message):
                print "Incorrect message instance: %s" % message
            return self.messages.has_key(message.get_name())

    def add_message(self, message):
        if type(message) == StringType:
            message = Message(message)
        if self.has_message(message):
            print "Message '%s' has been already added" % message.get_name()
            return
        self.messages[ message.get_name() ] = message
        return message

    def add_messages(self, messages):
        for message in messages:
            self.add_message(message)

    def get_message(self, message):
        if type(message) != StringType:
            return None
        if self.has_message(message):
            return self.messages[message]
        return None

    def get_messages(self):
        return self.messages.values()

    def has_thread(self, thread):
        if type(thread) == StringType:
            return self.threads.has_key(thread)
        elif type(thread) == InstanceType:
            if not isinstance(thread, Thread):
                print "Incorrect thread instance: %s" % thread
                return
            return self.threads.has_key(thread.get_name())

    def get_thread(self, thread):
        if type(thread) != StringType:
            return None
        if self.has_thread(thread):
            return self.threads[thread]
        return None

    def get_threads(self):
        return self.threads.values()

    def add_thread(self, thread):
        if self.has_thread(thread):
            print "Thread '%s' has been already added" % thread.get_name()
            return
        if type(thread) == StringType:
            thread = Thread(thread)
        self.threads[ thread.get_name() ] = thread
        return thread

    def add_threads(self, threads):
        for thread in threads:
            self.add_thread(thread)

    def add_module(self, mod_name):
        __import__(mod_name)
        mod = sys.modules[mod_name]
        mod_class_name = mod.__name__.split('.').pop().upper()
        try:
            mod_class = getattr(mod, mod_class_name)
        except AttributeError:
            print "Module %s should have class %s" % (mod_name, mod_class_name)
            raise
        self.modules[mod_name] = mod_class(self)

    def get_module(self, module_name):
        pass

    def get_modules(self):
        return self.modules.values()

    def delete_module(self, module_name):
        pass

