
__copyright__ = "Copyright (c) 2011 Sladeware LLC"

import sys
import os

# These are needed in a couple of spots, so just compute them once.
PREFIX = os.path.normpath(sys.prefix)
EXEC_PREFIX = os.path.normpath(sys.exec_prefix)

def get_python_version():
    """Return a string containing the major and minor Python version,
    leaving off the patchlevel.  Sample return values could be '1.5'
    or '2.2'.
    """
    return sys.version[:3]

def get_python_lib(plat_specific=0, standard_lib=0, prefix=None):
    """Return the directory containing the Python library (standard or
    site additions).

    If 'plat_specific' is true, return the directory containing
    platform-specific modules, i.e. any module from a non-pure-Python
    module distribution; otherwise, return the platform-shared library
    directory.  If 'standard_lib' is true, return the directory
    containing standard Python library modules; otherwise, return the
    directory for site-specific modules.

    If 'prefix' is supplied, use it instead of sys.prefix or
    sys.exec_prefix -- i.e., ignore 'plat_specific'.
    """
    if prefix is None:
        prefix = plat_specific and EXEC_PREFIX or PREFIX

    if os.name == "posix":
        libpython = os.path.join(prefix,
                                 "lib", "python" + get_python_version())
        if standard_lib:
            return libpython
        else:
            return os.path.join(libpython, "site-packages")

    elif os.name == "nt":
        if standard_lib:
            return os.path.join(prefix, "Lib")
        else:
            if get_python_version() < "2.2":
                return prefix
            else:
                return os.path.join(prefix, "Lib", "site-packages")

    elif os.name == "os2":
        if standard_lib:
            return os.path.join(prefix, "Lib")
        else:
            return os.path.join(prefix, "Lib", "site-packages")

    else:
        raise Exception(
            "I don't know where Python installs its library "
            "on platform '%s'" % os.name)

BB_PACKAGE_NAME = 'bb'
BB_PACKAGE_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

BB_PACKAGE_PATH = os.path.join(BB_PACKAGE_DIR, BB_PACKAGE_NAME)

if not os.path.exists(BB_PACKAGE_PATH):
    print "Can not find '%s'" % BB_PACKAGE_PATH
    exit(1)

if os.path.exists(os.path.join(get_python_lib(), BB_PACKAGE_NAME)):
    print "Removing", os.path.join(get_python_lib(), BB_PACKAGE_NAME)
    os.unlink(os.path.join(get_python_lib(), BB_PACKAGE_NAME))

print "%s --> %s" % (BB_PACKAGE_PATH, os.path.join(get_python_lib(), BB_PACKAGE_NAME))
os.symlink(BB_PACKAGE_PATH, os.path.join(get_python_lib(), BB_PACKAGE_NAME))

