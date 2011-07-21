#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Slade Maurer, Alexander Sviridenko"

import types

from bb.apps.utils.type_verification import verify_list

processes = {}
options = {}

SIMULATION_MODE = 0x1
DEV_MODE = 0x3

MODE = DEV_MODE

def select_mode(new_mode):
    global MODE
    MODE = new_mode

def get_mode():
    global MODE
    return MODE

def new_application(*args, **kargs):
    return Application(*args, **kargs)

def new_process(*args, **kargs):
    return Process(*args, **kargs)

class Process:
    def __init__(self, name, kernel=None):
        from bb import os
        self.__name = name
        self.__hardware = os.Hardware()
        self.__kernel = kernel

    def get_hardware(self):
        return self.__hardware

    def select_kernel(self, kernel):
        self.__kernel = kernel
        return kernel

    def get_kernel(self):
        return self.__kernel

    def run(self):
        self.__kernel.start()

class Application:
    def __init__(self):
        self.__processes = {}

    def add_process(self, name):
        process = Process(name)
        self.__processes[name] = process
        return process

    def run(self):
        for (name, process) in self.__processes.items():
            __import__(name)

import bb.app.setup

