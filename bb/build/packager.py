#!/usr/bin/env python

import os.path
import types
import inspect

from bb.lib.utils import typecheck
from bb.build import toolchain_manager

_storage = dict()

class Package(object):
    FILES = ()

    def __init__(self):
        self._files = list()
        self._context = dict()
        if self.FILES:
            self.add_files(self.FILES)

    @property
    def context(self):
        return self._context

    def add_files(self, files):
        for file in files:
            self.add_file(file)

    def get_files(self):
        return self._files

    def add_file(self, file):
        if not os.path.exists(file):
            package_file = inspect.getsourcefile(self.__class__)
            package_dirname = os.path.dirname(package_file)
            alternative_file = os.path.join(package_dirname, file)
            if not os.path.exists(alternative_file):
                print "WARNING: file '%s' cannot be found" % file
                return
            file = alternative_file
        self._files.append(file)

    def on_unpack(self):
        raise NotImplementedError

def get_object_packages(object_instance_or_class):
    packages = list()
    object_class = None
    if typecheck.is_class(object_instance_or_class):
        object_class = object_instance_or_class.__class__
    if not object_class in _storage:
        return []
    for toolchain, package in _storage[object_class].items():
        packages.append(package)
    return packages

def get_supported_toolchains(object_instance_or_class):
    global _storage
    toolchains = list()
    key = object_instance_or_class
    if not key in _storage:
        # TODO: check whether it's class or not
        key = object_instance_or_class.__class__
        if not key in _storage:
            return []
    for toolchain, package in _storage[key].items():
        toolchains.append(toolchain)
    return toolchains

def get_package(object_instance_or_class, toolchain_class_or_name):
    package_class = get_package_class(object_instance_or_class, toolchain_class_or_name)
    if not package_class:
        return None
    return package_class()

def get_package_class(object_instance_or_class, toolchain_class_or_name):
    global _storage
    toolchain_class = None
    if typecheck.is_class(toolchain_class_or_name):
        toolchain_class = toolchain_class_or_name
    else:
        toolchain_class = toolchain_manager.get_toolchain_by_name(toolchain_class_or_name)
    if not _storage.get(object_instance_or_class, None):
        if not typecheck.is_class(object_instance_or_class):
            return get_package_class(object_instance_or_class.__class__,
                                     toolchain_class_or_name)
        return None
    return _storage[object_instance_or_class].get(toolchain_class, None)

def pack(object_instance_or_class, toolchain_class_or_name, package_class=None):
    global _storage
    toolchain_class = None
    if typecheck.is_string(toolchain_class_or_name):
        toolchain_class = toolchain_manager.get_toolchain_class_by_name(toolchain_class_or_name)
        if not toolchain_class:
            raise Exception('Toolchain "%s" cannot be found' % toolchain_class_or_name)
    elif typecheck.is_class(toolchain_class_or_name):
        toolchain_class = toolchain_class_or_name
    else:
        raise Exception("toolchain_class_or_name not a class or name")
    def store(key, value):
        if not _storage.get(object_instance_or_class, None):
            _storage[object_instance_or_class] = dict()
        _storage[object_instance_or_class][key] = value

    if package_class:
        store(toolchain_class, package_class)
        return
    # As decorator
    def catcher(package_class):
        store(toolchain_class, package_class)
        return package_class
    return catcher
