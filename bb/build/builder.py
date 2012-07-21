#!/usr/bin/env python

import math
import logging

import bb
from bb.build import packager

logging.basicConfig(level=logging.DEBUG)

_application = None
_dependency_injectors = dict()
_objects = list()

def set_application(application):
    global _application
    if not isinstance(application, bb.Application):
        raise Exception("Must be bb.Application")
    _application = application

def get_application():
    global _application
    return _application

def build(application=None):
    if application:
        set_application(application)
    application = get_application()
    if not application:
        logging.error("Application must be provided")
        return
    if not application.get_num_mappings():
        logging.error("Nothing to build. Please, add at least one mapping "\
            "to this application.")
        return
    logging.debug("Build application")
    for mapping in application.get_mappings():
        _build_mapping(mapping)

def _build_mapping(mapping):
    if not isinstance(mapping, bb.Mapping):
        raise Exception("Must be bb.Mapping")
    logging.debug("Build mapping %s", mapping.get_name())
    if not mapping.get_num_threads():
        logging.error("Mapping", mapping.get_name(), "doesn't have threads")
        return
    print "*", "number of threads", "=", mapping.get_num_threads()
    processor = mapping.get_processor()
    if not processor:
        print "Mapping", mapping.get_name(), "doesn't connected to any processor"
        return
    print "*", "processor", "=", str(processor)
    cores = processor.get_cores()
    # Some cores can be disabled or not defined
    active_cores = list()
    for core_id in range(len(cores)):
        if cores[core_id]:
            active_cores.append(core_id)
    if not active_cores:
        print "Processor does not have active cores"
        return
    threads_per_core = default_thread_distribution(mapping.get_threads(), active_cores)
    print "Thread distribution:"
    for i in range(len(threads_per_core)):
        if not threads_per_core[i]:
            continue
        print "\t", str(processor.get_core(i)), ":", [str(_) for _ in threads_per_core[i]]
    os_class = mapping.get_os_class()
    for i in range(len(threads_per_core)):
        core_id = active_cores[i]
        core = cores[core_id]
        _build_os(os_class, threads_per_core[core_id])

def _build_os(os_class, threads):
    print "Build OS"
    os = os_class(threads)
    objects = assemble(os)
    toolchain_class = _select_toolchain_class(objects)
    print "Use toolchain:", toolchain_class
    toolchain = toolchain_class()
    print "Build packages"
    packages = list()
    for obj in objects:
        package = packager.get_package(obj, toolchain_class)
        package.context['object'] = obj
        package.context['toolchain'] = toolchain
        try:
            package.on_unpack()
        except NotImplementedError, e:
            pass
        toolchain.add_sources(package.get_files())
        packages.append(package)
    for package in packages:
        try:
            package.on_build()
        except Exception, e:
            pass
    toolchain.build()

def default_thread_distribution(threads, cores):
    step = int(math.ceil(float(len(threads)) / float(len(cores))))
    return [threads[x : x + step] for x in xrange(0, len(threads), step)]

def _select_toolchain_class(objects):
    available_toolchains = set(packager.get_supported_toolchains(objects[0]))
    for obj in objects:
        supported_toolchains = set(packager.get_supported_toolchains(obj))
        if not supported_toolchains:
            print "Object", obj, "does not have supported toolchains"
            return False
        available_toolchains = available_toolchains.intersection(supported_toolchains)
        if not available_toolchains:
            print "No common toolchains for an objects were found"
            return None
    print "Available toolchains:", list(available_toolchains)
    return list(available_toolchains)[0]

def dependency_injector(obj):
    def _(injector):
        set_dependency_injector(obj, injector)
        return injector
    return _

def set_dependency_injector(obj, injector):
    global _dependency_injector
    _dependency_injectors[obj] = injector

def get_dependency_injector(obj):
    global _dependency_injectors
    # TODO: what if obj is class
    obj_class = obj.__class__
    return _dependency_injectors.get(obj_class, None)

def assemble(target):
    global _objects
    resolve_dependencies(target)
    print len(_objects), "object(s) to be built"
    return _objects

def resolve_dependencies(target):
    global _objects
    _objects = list()
    _resolve_dependencies(target)

def _resolve_dependencies(target):
    global _objects
    _objects.append(target)
    injector = get_dependency_injector(target)
    if injector:
        dependencies = injector(target)
        # TODO: check list
        for obj in dependencies:
            _resolve_dependencies(obj)
