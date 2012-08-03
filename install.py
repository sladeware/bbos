#!/usr/bib/env python

"""Initially based on sysconfig.py from distutils package, with
a few improvements.
"""

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

import os
import sys

REQUIRED_PYTHON_MODULES = {
  "serial": "please download and install pyserial from http://pyserial.sourceforge.net",
  "networkx": "please download and install networkx library from http://networkx.lanl.gov",
}

# These are needed in a couple of spots, so just compute them once.
PREFIX = os.path.normpath(sys.prefix)
EXEC_PREFIX = os.path.normpath(sys.exec_prefix)

_config_vars = None

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
    raise Exception("I don't know where Python installs its library "
                    "on platform '%s'" % os.name)

def _init_posix():
  """Initialize the module as appropriate for POSIX systems."""
  global _config_vars
  _config_vars = {
    'LIBDEST': get_python_lib(plat_specific=0, standard_lib=1),
    'CC': 'gcc',
    'CXX': 'g++',
    'OPT': '',
    'CFLAGS': '' ,
    'EXTRA_CFLAGS': '',
    'BASECFLAGS': '',
    'CCSHARED': '',
    'LDSHARED': '',
    'SO': '.so',
    'BINDIR': os.path.dirname(os.path.realpath(sys.executable)),
    }
  return _config_vars

def _init_nt():
  """Initialize the module as appropriate for NT"""
  global _config_vars
  _config_vars = {
    # set basic install directories
    'LIBDEST': get_python_lib(plat_specific=0, standard_lib=1),
    'BINLIBDEST': get_python_lib(plat_specific=1, standard_lib=1),
    # XXX hmmm.. a normal install puts include files here
    'INCLUDEPY': get_python_inc(plat_specific=0),
    'SO': '.pyd',
    'EXE': ".exe",
    'VERSION': get_python_version().replace(".", ""),
    'BINDIR': os.path.dirname(os.path.realpath(sys.executable)),
    }
  return _config_vars

def _init_mac():
  """Initialize the module as appropriate for Macintosh systems."""
  global _config_vars
  _config_vars = {
    # set basic install directories
    'LIBDEST': get_python_lib(plat_specific=0, standard_lib=1),
    'BINLIBDEST': get_python_lib(plat_specific=1, standard_lib=1),
    # XXX hmmm.. a normal install puts include files here
    'INCLUDEPY': get_python_inc(plat_specific=0),
    # XXX are these used anywhere?
    'install_lib': os.path.join(EXEC_PREFIX, "Lib"),
    'install_platlib': os.path.join(EXEC_PREFIX, "Mac", "Lib"),
    # These are used by the extension module build
    'srcdir': ':',
    }
  import MacOS
  if not hasattr(MacOS, 'runtimemodel'):
    _config_vars['SO'] = '.ppc.slb'
  else:
    _config_vars['SO'] = '.%s.slb' % MacOS.runtimemodel
  return _config_vars

def _init_os2():
  """Initialize the module as appropriate for OS/2"""
  global _config_vars
  _config_vars = {
    # set basic install directories
    'LIBDEST': get_python_lib(plat_specific=0, standard_lib=1),
    'BINLIBDEST': get_python_lib(plat_specific=1, standard_lib=1),
    # XXX hmmm.. a normal install puts include files here
    'INCLUDEPY': get_python_inc(plat_specific=0),
    'SO': '.pyd',
    'EXE': ".exe",
    }
  return _config_vars

def get_config_vars(*args):
  """With no arguments, return a dictionary of all configuration
  variables relevant for the current platform.  Generally this includes
  everything needed to build extensions and install both pure modules and
  extensions.  On Unix, this means every variable defined in Python's
  installed Makefile; on Windows and Mac OS it's a much smaller set.

  With arguments, return a list of values that result from looking up
  each argument in the configuration variable dictionary.
  """
  global _config_vars
  if _config_vars is None:
    if   os.name == 'posix': _config_vars = _init_posix()
    elif os.name == 'mac'  : _config_vars = _init_mac()
    elif os.name == 'nt'   : _config_vars = _init_nt()
    elif os.name == 'os2'  : _config_vars = _init_os2()
    # Normalized versions of prefix and exec_prefix are handy to have;
    # in fact, these are the standard versions used most places in the
    # Distutils.
    _config_vars['prefix'] = PREFIX
    _config_vars['exec_prefix'] = EXEC_PREFIX
    if sys.platform == 'darwin':
      kernel_version = os.uname()[2] # Kernel version (8.4.3)
      major_version = int(kernel_version.split('.')[0])
      if major_version < 8:
        # On Mac OS X before 10.4, check if -arch and -isysroot
        # are in CFLAGS or LDFLAGS and remove them if they are.
        # This is needed when building extensions on a 10.3 system
        # using a universal build of python.
        for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED',
                    # a number of derived variables. These need to be
                    # patched up as well.
                    'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
          flags = _config_vars[key]
          flags = re.sub('-arch\s+\w+\s', ' ', flags)
          flags = re.sub('-isysroot [^ \t]*', ' ', flags)
          _config_vars[key] = flags
      else:
        # Allow the user to override the architecture flags using
        # an environment variable.
        # NOTE: This name was introduced by Apple in OSX 10.5 and
        # is used by several scripting languages distributed with
        # that OS release.
        if 'ARCHFLAGS' in os.environ:
          arch = os.environ['ARCHFLAGS']
          for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED',
                      # a number of derived variables. These need to be
                      # patched up as well.
                      'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
            flags = _config_vars[key]
            flags = re.sub('-arch\s+\w+\s', ' ', flags)
            flags = flags + ' ' + arch
            _config_vars[key] = flags
        # If we're on OSX 10.5 or later and the user tries to
        # compiles an extension using an SDK that is not present
        # on the current machine it is better to not use an SDK
        # than to fail.
        #
        # The major usecase for this is users using a Python.org
        # binary installer  on OSX 10.6: that installer uses
        # the 10.4u SDK, but that SDK is not installed by default
        # when you install Xcode.
        m = re.search('-isysroot\s+(\S+)', _config_vars['CFLAGS'])
        if m is not None:
          sdk = m.group(1)
          if not os.path.exists(sdk):
            for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED',
                        # a number of derived variables. These need to be
                        # patched up as well.
                        'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
              flags = _config_vars[key]
              flags = re.sub('-isysroot\s+\S+(\s|$)', ' ', flags)
              _config_vars[key] = flags
  if args:
    vals = []
    for name in args:
      vals.append(_config_vars.get(name))
    return vals
  else:
    return _config_vars

def banner():
  print " ____  ____    ___           _        _ _ "
  print "| __ )| __ )  |_ _|_ __  ___| |_ __ _| | |"
  print "|  _ \|  _ \   | || '_ \/ __| __/ _` | | |"
  print "| |_) | |_) |  | || | | \__ \ || (_| | | |"
  print "|____/|____/  |___|_| |_|___/\__\__,_|_|_|"
  print

def check_dependencies():
  ok = True
  print "Checking for dependencies:"
  for mod_name, err_msg in REQUIRED_PYTHON_MODULES.items():
    try:
      __import__(mod_name)
      print "* '%s'... [OK]" % mod_name
    except ImportError:
      msg = "[NOT FOUND]"
      if err_msg:
        msg = err_msg
      print "* '%s'... %s" % (mod_name, msg)
      ok = False
  return ok

BB_HOME = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
BB_PACKAGE_NAME = 'bb'
BB_PACKAGE_PATH = os.path.join(BB_HOME, BB_PACKAGE_NAME)

# Test BB_PACKAGE_PATH
if not os.path.exists(BB_PACKAGE_PATH):
  print "Can not find bb package '%s'" % BB_PACKAGE_PATH
  sys.exit(1)
else:
  print "Package path:", BB_PACKAGE_PATH

def main():
  banner()
  # NOTE: on this moment we will only create a links
  (libdest, ) = get_config_vars('LIBDEST')
  bb_package_link_path = os.path.join(libdest, BB_PACKAGE_NAME)
  if os.path.exists(bb_package_link_path) or os.path.lexists(bb_package_link_path):
    print "Removing old link:", bb_package_link_path
    os.unlink(bb_package_link_path)
  if not check_dependencies():
    print "Sorry, but BB cannot be installed"
    exit(1)
  print "Creating a link to BB package:", bb_package_link_path
  os.symlink(BB_PACKAGE_PATH, bb_package_link_path)
  # Create link to the BB script
  (bindir, ) = get_config_vars('BINDIR')
  bb_script_link_path = os.path.join(bindir, 'bb')
  print "Creating a link to BB script:", bb_script_link_path
  if os.path.exists(bb_script_link_path) or os.path.lexists(bb_script_link_path):
    print "Removing old link:", bb_script_link_path
    os.unlink(bb_script_link_path)
  os.link('./scripts/bionicbunny.py', bb_script_link_path)
  return 0

if __name__ == '__main__':
  sys.exit(main())
