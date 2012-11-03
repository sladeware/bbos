# Initialization
AC_INIT([bb], [0.1], [], [], [info@bionicbunny.org])
AM_MAINTAINER_MODE([enable])
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
#AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE

AX_CHECK_GNU_MAKE()

# Check for python...
m4_include([m4/python.m4])
PY_PROG_PYTHON()
PY_PYTHON_VERSION()
PY_PYTHON_PREFIX()
PY_PYTHON_IMPORT_CHECK([networkx])

AC_PROG_LIBTOOL
AC_CONFIG_FILES([Makefile scripts/bb.sh])
AC_OUTPUT
