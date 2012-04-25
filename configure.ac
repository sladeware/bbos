# Initialization
AC_INIT([bb], [0.1], [], [], [mail@bionicbunny.org])
AC_CONFIG_AUX_DIR([.])
AM_INIT_AUTOMAKE([foreign no-define])

AX_CHECK_GNU_MAKE()

# Check for python...
m4_include([m4/python.m4])
PY_PROG_PYTHON()
PY_PYTHON_VERSION()
PY_PYTHON_PREFIX()
PY_PYTHON_IMPORT_CHECK([networkx])

AC_CONFIG_FILES([Makefile])

AC_OUTPUT
