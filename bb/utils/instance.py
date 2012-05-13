#!/usr/bin/env python

__copyright__ = "Copyright (c) 2012 Sladeware LLC"

import weakref

class InstanceTracking(object):
    __refs__ = dict()

    def __init__(self):
        if self.__class__ not in self.__refs__:
            self.__refs__[self.__class__] = list()
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_next_instance(cls):
        for inst_ref in cls.__refs__.get(cls, list()):
            inst = inst_ref()
            if inst is not None:
                yield inst

    @classmethod
    def get_instances(cls):
        all_instances = list()
        for _ in cls.get_next_instance():
            all_instances.append(_)
        return all_instances

    @classmethod
    def get_num_instances(cls):
        instances = cls.get_instances()
        return len(instances)
