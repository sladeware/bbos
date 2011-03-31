"""Provide access to Python's configuration information.  The specific
configuration variables available depend heavily on the platform and
configuration.  The values may be retrieved using
get_config_var(name), and the list of variables is available via
get_config_vars().keys().  Additional convenience functions are also
available.

Written by:   Fred L. Drake, Jr.
Email:        <fdrake@acm.org>
"""

__revision__ = "$Id: sysconfig.py 83688 2010-08-03 21:18:06Z mark.dickinson $"

import os
import re
import string
import sys

from builder.errors import DistutilsPlatformError

# These are needed in a couple of spots, so just compute them once.
PREFIX = os.path.normpath(sys.prefix)
EXEC_PREFIX = os.path.normpath(sys.exec_prefix)

# Path to the base directory of the project. On Windows the binary may
# live in project/PCBuild9.  If we're dealing with an x64 Windows build,
# it'll live in project/PCbuild/amd64.
project_base = os.path.dirname(os.path.realpath(sys.executable))
if os.name == "nt" and "pcbuild" in project_base[-8:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir))
# PC/VS7.1
if os.name == "nt" and "\\pc\\v" in project_base[-10:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir,
                                                os.path.pardir))
# PC/AMD64
if os.name == "nt" and "\\pcbuild\\amd64" in project_base[-14:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir,
                                                os.path.pardir))

# python_build: (Boolean) if true, we're either building Python or
# building an extension with an un-installed Python, so we use
# different (hard-wired) directories.
# Setup.local is available for Makefile builds including VPATH builds,
# Setup.dist is available on Windows
def _python_build():
    for fn in ("Setup.dist", "Setup.local"):
        if os.path.isfile(os.path.join(project_base, "Modules", fn)):
            return True
    return False
python_build = _python_build()


def get_python_version():
    """Return a string containing the major and minor Python version,
    leaving off the patchlevel.  Sample return values could be '1.5'
    or '2.2'.
    """
    return sys.version[:3]


def get_python_inc(plat_specific=0, prefix=None):
    """Return the directory containing installed Python header files.

    If 'plat_specific' is false (the default), this is the path to the
    non-platform-specific header files, i.e. Python.h and so on;
    otherwise, this is the path to platform-specific header files
    (namely pyconfig.h).

    If 'prefix' is supplied, use it instead of sys.prefix or
    sys.exec_prefix -- i.e., ignore 'plat_specific'.
    """
    if prefix is None:
        prefix = plat_specific and EXEC_PREFIX or PREFIX

    if os.name == "posix":
        if python_build:
            buildir = os.path.dirname(os.path.realpath(sys.executable))
            if plat_specific:
                # python.h is located in the buildir
                inc_dir = buildir
            else:
                # the source dir is relative to the buildir
                srcdir = os.path.abspath(os.path.join(buildir,
                                         get_config_var('srcdir')))
                # Include is located in the srcdir
                inc_dir = os.path.join(srcdir, "Include")
            return inc_dir
        return os.path.join(prefix, "include",
                            "python" + get_python_version() + (sys.pydebug and '_d' or ''))
    elif os.name == "nt":
        return os.path.join(prefix, "include")
    elif os.name == "mac":
        if plat_specific:
            return os.path.join(prefix, "Mac", "Include")
        else:
            return os.path.join(prefix, "Include")
    elif os.name == "os2":
        return os.path.join(prefix, "Include")
    else:
        raise DistutilsPlatformError(
            "I don't know where Python installs its C header files "
            "on platform '%s'" % os.name)


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
    is_default_prefix = not prefix or os.path.normpath(prefix) in ('/usr', '/usr/local')
    if prefix is None:
        prefix = plat_specific and EXEC_PREFIX or PREFIX

    if os.name == "posix":
        libpython = os.path.join(prefix,
                                 "lib", "python" + get_python_version())
        if standard_lib:
            return libpython
        elif is_default_prefix and 'PYTHONUSERBASE' not in os.environ and 'real_prefix' not in sys.__dict__:
            return os.path.join(libpython, "dist-packages")
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

    elif os.name == "mac":
        if plat_specific:
            if standard_lib:
                return os.path.join(prefix, "Lib", "lib-dynload")
            else:
                return os.path.join(prefix, "Lib", "site-packages")
        else:
            if standard_lib:
                return os.path.join(prefix, "Lib")
            else:
                return os.path.join(prefix, "Lib", "site-packages")

    elif os.name == "os2":
        if standard_lib:
            return os.path.join(prefix, "Lib")
        else:
            return os.path.join(prefix, "Lib", "site-packages")

    else:
        raise DistutilsPlatformError(
            "I don't know where Python installs its library "
            "on platform '%s'" % os.name)


def customize_compiler(compiler):
    """Do any platform-specific customization of a CCompiler instance.

    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
    if compiler.compiler_type == "unix":
        (cc, cxx, opt, cflags, opt, extra_cflags, basecflags, ccshared, ldshared, so_ext) = \
            get_config_vars('CC', 'CXX', 'OPT', 'CFLAGS',
                            'OPT', 'EXTRA_CFLAGS', 'BASECFLAGS',
                            'CCSHARED', 'LDSHARED', 'SO')
        
        if 'CC' in os.environ:
            cc = os.environ['CC']
        if 'CXX' in os.environ:
            cxx = os.environ['CXX']
        if 'LDSHARED' in os.environ:
            ldshared = os.environ['LDSHARED']
        if 'CPP' in os.environ:
            cpp = os.environ['CPP']
        else:
            cpp = cc + " -E"           # not always
        if 'LDFLAGS' in os.environ:
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if 'BASECFLAGS' in os.environ:
            basecflags = os.environ['BASECFLAGS']
        if 'OPT' in os.environ:
            opt = os.environ['OPT']
        cflags = ' '.join(str(x) for x in (basecflags, opt, extra_cflags) if x)
        if 'CFLAGS' in os.environ:
            cflags = ' '.join(str(x) for x in (basecflags, opt, os.environ['CFLAGS'], extra_cflags) if x)
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if 'CPPFLAGS' in os.environ:
            cpp = cpp + ' ' + os.environ['CPPFLAGS']
            cflags = cflags + ' ' + os.environ['CPPFLAGS']
            ldshared = ldshared + ' ' + os.environ['CPPFLAGS']

        cc_cmd = cc + ' ' + cflags
        compiler.set_executables(
            preprocessor=cpp,
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ccshared,
            compiler_cxx=cxx,
            linker_so=ldshared,
            linker_exe=cc)

        compiler.shared_lib_extension = so_ext


_config_vars = None

def _init_posix():
    """Initialize the module as appropriate for POSIX systems."""
    g = {}

    g['CC'] = 'gcc'
    g['CXX'] = 'g++'
    g['OPT'] = ''
    g['CFLAGS'] = '' 
    g['EXTRA_CFLAGS'] = ''
    g['BASECFLAGS'] = ''
    g['CCSHARED'] = ''
    g['LDSHARED'] = ''
    g['SO'] = '.so'

    global _config_vars
    _config_vars = g

def _init_nt():
    """Initialize the module as appropriate for NT"""
    g = {}
    # set basic install directories
    g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
    g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)

    # XXX hmmm.. a normal install puts include files here
    g['INCLUDEPY'] = get_python_inc(plat_specific=0)

    g['SO'] = '.pyd'
    g['EXE'] = ".exe"
    g['VERSION'] = get_python_version().replace(".", "")
    g['BINDIR'] = os.path.dirname(os.path.realpath(sys.executable))

    global _config_vars
    _config_vars = g


def _init_mac():
    """Initialize the module as appropriate for Macintosh systems"""
    g = {}
    # set basic install directories
    g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
    g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)

    # XXX hmmm.. a normal install puts include files here
    g['INCLUDEPY'] = get_python_inc(plat_specific=0)

    import MacOS
    if not hasattr(MacOS, 'runtimemodel'):
        g['SO'] = '.ppc.slb'
    else:
        g['SO'] = '.%s.slb' % MacOS.runtimemodel

    # XXX are these used anywhere?
    g['install_lib'] = os.path.join(EXEC_PREFIX, "Lib")
    g['install_platlib'] = os.path.join(EXEC_PREFIX, "Mac", "Lib")

    # These are used by the extension module build
    g['srcdir'] = ':'
    global _config_vars
    _config_vars = g


def _init_os2():
    """Initialize the module as appropriate for OS/2"""
    g = {}
    # set basic install directories
    g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
    g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)

    # XXX hmmm.. a normal install puts include files here
    g['INCLUDEPY'] = get_python_inc(plat_specific=0)

    g['SO'] = '.pyd'
    g['EXE'] = ".exe"

    global _config_vars
    _config_vars = g


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
        func = globals().get("_init_" + os.name)
        if func:
            func()
        else:
            _config_vars = {}

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
                #
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

def get_config_var(name):
    """Return the value of a single variable using the dictionary
    returned by 'get_config_vars()'.  Equivalent to
    get_config_vars().get(name)
    """
    return get_config_vars().get(name)
