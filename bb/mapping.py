#!/usr/bin/env python

import bb
from bb.hardware.devices.processors import Processor
from bb.lib.utils import typecheck

class Mapping(object):
    OS_CLASS = bb.os.OS

    def __init__(self, name, os_class=None, processor=None):
        self._name = None
        self._threads = dict()
        self._os_class = None
        self._is_simulation_mode = False
        self._processor = None
        # NOTE: for now we will force user to provide a name
        self.set_name(name)
        if os_class:
            self.set_os_class(os_class)
        else:
            self.set_os_class(self.OS_CLASS)
        if processor:
            self.set_processor(processor)

    def set_name(self, name):
        if not typecheck.is_string(name):
            raise Exception("name must be string")
        self._name = name

    def get_name(self):
        return self._name

    def register_thread(self, thread):
        if not isinstance(thread, bb.Thread):
            raise Exception("Must be derived from bb.Thread")
        self._threads[ thread.get_name() ] = thread

    def register_threads(self, threads):
        for thread in threads:
            self.register_thread(thread)

    def get_num_threads(self):
        return len(self.get_threads())

    def get_threads(self):
        return self._threads.values()

    def set_simulation_mode(self):
        self._is_simulation_mode = True

    def is_simulation_mode(self):
        return self._is_simulation_mode

    def get_processor(self):
        return self._processor

    def set_processor(self, processor):
        if not isinstance(processor, Processor):
            raise Exception("Requires Processor class.")
        self._processor = processor

    def set_os_class(self, os_class):
        if not issubclass(os_class, bb.os.OS):
            raise Exception("Must be derived from bbos.OS class:", os_class)
        self._os_class = os_class

    def get_os_class(self):
        return self._os_class
