#
# Copyright (c) 2011 Alexander Sviridenko
#

"""Utilities for module control."""

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

def get_dir(module_name=None):
    """Return path to directory from where script with module was invoked. If 
    module_name does not provided the caller's module will be used."""
    if not module_name:
        module_name = caller()[1]
    module = get_object(module_name)
    file_name = inspect.getfile(module)
    return os.path.abspath(os.path.dirname(os.path.realpath(file_name)))

def get_file(module_name=None, file_name=None):
    """Return the name of the (text or binary) file in which the module 
    module_name was defined. If module_name does not provided the caller's 
    module will be used. 
    
    This function allows to find files next to module file. For example, 
    the path to the setup.py from a given distribution package can be obtained 
    as follows: module.get_file(__name__, 'setup.py')."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    if not file_name:
        file_name = inspect.getfile(module)
    return os.path.abspath(os.path.join(get_dir(module_name), file_name))

def get_classes(module_name=None):
    """Return all the classes of a module module_name in a list of (name, value) 
    pairs. The list does not include imported or built-in classes. If module 
    does not provided the caller's module will be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    classes = {}
    for name, obj in inspect.getmembers(module):
	if inspect.isclass(obj) and (obj.__module__ == module_name):
	    classes[name] = obj
    return classes

def get_object(module_name=None):
    """Return module object of a module module_name. If module_name does not provided 
    the caller's module will be used."""
    if type(module_name) is types.ModuleType:
	return module_name
    elif type(module_name) is types.NoneType:
	module_name = caller()[1]
    elif type(module_name) is not types.StringType:
	raise TypeError("Unknown type")
    if not sys.modules.has_key(module_name):
	raise ModuleError("Module '%s' does not exist" % module_name)
    return sys.modules[module_name]

def get_name(module_name=None, default=None):
    """Return module name. If the name attribute does not exist, default is returned. 
    By default default is None. If module does not provided the caller's module will 
    be used."""
    if not module_name:
	module_name = caller()[1]
	return module_name
    module = get_object(module_name)
    return getattr(module, '__name__', default)

# Version Management

def get_version(module_name=None, default=None):
    """Return module version. If the version attribute does not exist, default is 
    returned. If module_name does not provided the caller's module will be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    return getattr(module, '__version__', default)

def set_version(value, module_name=None):
    """Set module version. If module_name does not provided the caller's module will 
    be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    setattr(module, '__version__', value)

# Copyright Management

def get_copyright(module_name=None, default=None):
    """Return a string containing the copyright pertaining to the module module_name.
    If the copyright attribute does not exist, default is returned. If module_name 
    does not provided the caller's module will be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    return getattr(module, '__copyright__', default)

def set_copyright(value, module_name=None):
    """Set module copyright. If module_name does not provided the caller's module 
    will be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    setattr(module, '__copyright__', value)

# Doc Management

def get_doc(module_name=None, default=None):
    """Return the documentation string for a module module_name. If module_name 
    does not provided the caller's module will be used."""
    if not module_name:
	module_name = caller()[1]
    module = get_object(module_name)
    return inspect.getdoc(module) or default

"""
class Module(object):
    def __init__(self, mod=None):
	if not mod:
	    mod = inspect.getmodule(self)
	self.mod = module(mod)

    def get_name(self, default=None):
	return get_module_name(default, self.mod)

    def get_file(self):
	return get_module_file(self.mod)
    
    def get_version(self, default=None):
	return get_module_version(default, self.mod)

    def set_version(self, value):
	set_module_version(value, self.mod)

    def get_copyright(self, default=None):
	return get_module_copyright(default, self.mod)

    def set_copyright(self, value):
	set_module_copyright(value, self.mod)

    def get_module_doc(self, default=None):
	return get_module_doc(default, self.mod)
"""

set_version('0.2.0')
set_copyright('Copyright 2011 (c) Alexander Sviridenko')

if __name__ == '__main__':
    print "Module version:", get_version()
    print "Module copyright:", get_copyright()
    import os.path
    print get_file(__name__)

