#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__copyright__ = "Copyright (c) 2012 Sladeware LLC"
__author__ = "Oleksandr Sviridenko"

from bb.tools.compilers.compiler import Compiler

try:
  import MacOS
except ImportError, e:
  pass
import os
import sys

# These are needed in a several places, so just compute them once.
_PREFIX = os.path.normpath(sys.prefix)
_EXEC_PREFIX = os.path.normpath(sys.exec_prefix)

class _Config(dict):
  """Dictionary of all configuration variables relevant for the current
  platform.  Generally this includes everything needed to build extensions and
  install both pure modules and extensions. On Unix, this means every variable
  defined in Python's installed Makefile; on Windows and Mac OS it's a much
  smaller set.

  With arguments, return a list of values that result from looking up
  each argument in the configuration variable dictionary.
  """

  def __init__(self):
    dict.__init__(self)
    initializers = {
      'posix': self._init_posix,
      'mac': self._init_mac,
      'nt': self._init_nt,
      'os2': self._init_os2,
      }
    initializer = initializers[os.name]
    initializer()
    # Normalized versions of prefix and exec_prefix are handy to have;
    # in fact, these are the standard versions used most places in the
    # Distutils.
    self['prefix'] = _PREFIX
    self['exec_prefix'] = _EXEC_PREFIX
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
          flags = self[key]
          flags = re.sub('-arch\s+\w+\s', ' ', flags)
          flags = re.sub('-isysroot [^ \t]*', ' ', flags)
          self[key] = flags
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
            flags = self[key]
            flags = re.sub('-arch\s+\w+\s', ' ', flags)
            flags = flags + ' ' + arch
            self[key] = flags
        # If we're on OSX 10.5 or later and the user tries to
        # compiles an extension using an SDK that is not present
        # on the current machine it is better to not use an SDK
        # than to fail.
        #
        # The major usecase for this is users using a Python.org
        # binary installer  on OSX 10.6: that installer uses
        # the 10.4u SDK, but that SDK is not installed by default
        # when you install Xcode.
        m = re.search('-isysroot\s+(\S+)', self['CFLAGS'])
        if m is not None:
          sdk = m.group(1)
          if not os.path.exists(sdk):
            for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED',
                        # a number of derived variables. These need to be
                        # patched up as well.
                        'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
              flags = self[key]
              flags = re.sub('-isysroot\s+\S+(\s|$)', ' ', flags)
              self[key] = flags

  def _init_posix(self):
    """Initialize the module as appropriate for POSIX systems."""
    self.update(
      LIBDEST=self.get_lib_dir(plat_specific=0, standard_lib=1),
      CC='gcc',
      CXX='g++',
      OPT='',
      CFLAGS='' ,
      EXTRA_CFLAGS='',
      BASECFLAGS='',
      CCSHARED='',
      LDSHARED='',
      SO='.so',
      BINDIR=os.path.dirname(os.path.realpath(sys.executable)),
      )

  def _init_nt(self):
    """Initializes the module as appropriate for NT."""
    self.update(
      # Set basic install directories
      LIBDEST=python.get_lib(plat_specific=0, standard_lib=1),
      BINLIBDEST=python.get_lib(plat_specific=1, standard_lib=1),
      # TODO: hmmm.. a normal install puts include files here
      INCLUDEPY=python.get_inc(plat_specific=0),
      SO=".pyd",
      EXE=".exe",
      VERSION=python.get_version().replace(".", ""),
      BINDIR=os.path.dirname(os.path.realpath(sys.executable)),
      )

  def _init_mac(self):
    """Initialize the module as appropriate for Macintosh systems."""
    self.update(
      # set basic install directories
      LIBDEST=python.get_lib(plat_specific=0, standard_lib=1),
      BINLIBDEST=python.get_lib(plat_specific=1, standard_lib=1),
      # TODO: hmmm.. a normal install puts include files here
      INCLUDEPY=python.get_inc(plat_specific=0),
      # TOOD: are these used anywhere?
      install_lib=os.path.join(EXEC_PREFIX, "Lib"),
      install_platlib=os.path.join(EXEC_PREFIX, "Mac", "Lib"),
      # These are used by the extension module build
      srcdir=":",
      )
    if not hasattr(MacOS, 'runtimemodel'):
      self['SO'] = '.ppc.slb'
    else:
      self['SO'] = '.%s.slb' % MacOS.runtimemodel

  def _init_os2(self):
    """Initialize the module as appropriate for OS/2."""
    self.dict(
      LIBDEST=python.get_lib_dir(plat_specific=0, standard_lib=1),
      BINLIBDEST=python.get_lib(plat_specific=1, standard_lib=1),
      # TODO: hmmm.. a normal install puts include files here
      INCLUDEPY=python.get_inc_dir(plat_specific=0),
      SO=".pyd",
      EXE=".exe",
      )

  @classmethod
  def get_inc_dir(klass):
    pass

  @classmethod
  def get_lib_dir(klass, plat_specific=0, standard_lib=0, prefix=None):
    """Returns the directory containing the Python library (standard or site
    additions).

    If 'plat_specific' is true, return the directory containing
    platform-specific modules, i.e. any module from a non-pure-Python module
    distribution; otherwise, return the platform-shared library directory. If
    'standard_lib' is true, return the directory containing standard Python
    library modules; otherwise, return the directory for site-specific modules.

    If 'prefix' is supplied, use it instead of sys.prefix or sys.exec_prefix --
    i.e., ignore 'plat_specific'.
    """
    if prefix is None:
      prefix = plat_specific and _EXEC_PREFIX or _PREFIX
    if os.name == "posix":
      libpython = os.path.join(prefix, "lib", "python" + sys.version[:3])
      if standard_lib:
        return libpython
      else:
        return os.path.join(libpython, "site-packages")
    elif os.name == "nt":
      if standard_lib:
        return os.path.join(prefix, "Lib")
      else:
        if sys.version[:3] < "2.2":
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

class Python(Compiler):
  """Python compiler."""

  config = _Config()

  @classmethod
  def get_version(klass):
    """Returns a string containing the major and minor Python version, leaving
    off the patchlevel. Sample return values could be '1.5' or '2.2'.
    """
    return sys.version[:3]
