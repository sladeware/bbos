#!/usr/bin/env python

__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import inspect
import sys
import os.path
import types

class ModuleError(Exception):
    """The base class for the exceptions related to module."""

def caller():
    """Return the context of the current function call. Return a tuple
    (func_name, module_name, file_name, line)."""
    func_name= inspect.getouterframes(inspect.currentframe())[2][3]
    module_name = inspect.getmodule(inspect.stack()[2][0]).__name__
    file_name = inspect.getmodule(inspect.stack()[2][0]).__file__
    line = inspect.getouterframes(inspect.currentframe())[2][2]
    return (func_name, module_name, file_name, line)

def get_module(module_name=None):
    """Return module object of a module module_name. If module_name does not
    provided the caller's module will be used."""
    if type(module_name) is types.ModuleType:
        return module_name
    elif type(module_name) is types.NoneType:
        module_name = caller()[1]
    elif type(module_name) is not types.StringType:
        raise TypeError("Unknown type")
    if not sys.modules.has_key(module_name):
        raise ModuleError("Module '%s' does not exist" % module_name)
    return sys.modules[module_name]

def get_dir(module_name=None):
    """Return path to directory from where script with module was invoked. If
    module_name does not provided the caller's module will be used."""
    if not module_name:
        module_name = caller()[1]
    module = get_module(module_name)
    file_name = inspect.getfile(module)
    return os.path.abspath(os.path.dirname(os.path.realpath(file_name)))

def get_file(file_name=None, module_name=None):
    """Return the name of the (text or binary) file in which the module
    module_name was defined. If module_name does not provided the caller's
    module will be used.

    This function allows to find files next to module file. For example,
    the path to the setup.py from a given distribution package can be obtained
    as follows: module.get_file(__name__, 'setup.py')."""
    if not module_name:
	module_name = caller()[1]
    module = get_module(module_name)
    if not file_name:
        file_name = inspect.getfile(module)
    return os.path.abspath(os.path.join(get_dir(module_name), file_name))
