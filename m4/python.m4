dnl Macros to help with configuring Python extensions via autoconf.
dnl Copyright (c) 2012, Sladeware LLC

dnl Check for location of python.
AC_DEFUN([PY_PROG_PYTHON],
  [AC_ARG_WITH(python,
  [  --with-python=CMD       name of python executable],,[with_python=no])
  AC_MSG_CHECKING(for python)
  if test "x$with_python" != xno && test -x "$with_python"; then
    PYTHON="$with_python"
    AC_MSG_RESULT($PYTHON)
    AC_SUBST(PYTHON)
  else    
    AC_PATH_PROG(PYTHON, python, python)
    AC_MSG_RESULT($PYTHON)
  fi]
)

dnl Check for python version
AC_DEFUN([PY_PYTHON_VERSION],
  [AC_REQUIRE([PY_PROG_PYTHON])
  AC_MSG_CHECKING(python version)

  AC_CACHE_VAL(py_cv_major, [changequote((_,_))
    py_cv_major=`$PYTHON -c 'import sys; print str(sys.version_info[0])'`
    changequote([,])
  ])
  if test "$py_cv_major" -lt "2"; then
    AC_ERROR([You need at least python version 2.7])
  fi
  AC_CACHE_VAL(py_cv_minor, [changequote((_,_))
    py_cv_minor=`$PYTHON -c 'import sys; print str(sys.version_info[1])'`
    changequote([,])
  ])
  if test "$py_cv_minor" -lt "7"; then
    AC_ERROR([You need at least python version 2.7])
  fi

  PYTHON_VERSION="$py_cv_major.$py_cv_minor"
  AC_MSG_RESULT($PYTHON_VERSION)
  VERSION=$PYTHON_VERSION
  PY_VERSION="$py_cv_major$py_cv_minor"
  AC_SUBST(VERSION)
  AC_SUBST(PYTHON_VERSION)
  AC_SUBST(PY_VERSION)
])

dnl Check python installation prefix
AC_DEFUN([PY_PYTHON_PREFIX],
[AC_REQUIRE([PY_PROG_PYTHON])
AC_ARG_WITH(python-prefix,
[  --with-python-prefix=DIR
                          override the prefix for python],,
[with_python_prefix=no])
if test "x$with_python_prefix" != xno; then
  PYTHON_PREFIX="$with_python_prefix"
fi
AC_MSG_CHECKING(python installation prefix)
if test -z "$PYTHON_PREFIX"; then
  AC_CACHE_VAL(py_cv_python_prefix,
  [py_cv_python_prefix=`$PYTHON -c 'import sys; print sys.prefix'`])
else
  py_cv_python_prefix="$PYTHON_PREFIX"
fi
PYTHON_PREFIX="$py_cv_python_prefix"
AC_MSG_RESULT($PYTHON_PREFIX)
AC_SUBST(PYTHON_PREFIX)
prefix=$PYTHON_PREFIX
])

dnl Check python installation exec_prefix
AC_DEFUN([PY_PYTHON_EXEC_PREFIX],
[AC_REQUIRE([PY_PROG_PYTHON])
AC_ARG_WITH(python-prefix,
[  --with-python-exec-prefix=DIR
                          override the exec prefix for python],,
[with_python_exec_prefix=no])
if test "x$with_python_exec_prefix" != xno; then
  PYTHON_EXEC_PREFIX="$with_python_exec_prefix"
fi
AC_MSG_CHECKING(python installation exec_prefix)
if test -z "$PYTHON_EXEC_PREFIX"; then
  AC_CACHE_VAL(py_cv_python_exec_prefix,
  [py_cv_python_exec_prefix=`$PYTHON -c 'import sys; print sys.exec_prefix'`])
else
  py_cv_python_exec_prefix="$PYTHON_EXEC_PREFIX"
fi
PYTHON_EXEC_PREFIX="$py_cv_python_exec_prefix"
AC_MSG_RESULT($PYTHON_EXEC_PREFIX)
AC_SUBST(PYTHON_EXEC_PREFIX)
exec_prefix=$PYTHON_EXEC_PREFIX
])

AC_DEFUN([PY_PYTHON_IMPORT_CHECK],
  [
    module=$1
    AC_MSG_CHECKING(for Python module $module)
     rv=`$PYTHON -c "
try:
  import $module
except ImportError:
  exit(1)
exit(0)"`
    if test "$?" != "0"; then
        AC_MSG_RESULT(no)
        AC_ERROR([In order to use BB you need the following python module available  

$module

Please install this module and then rerun configure.])
    fi
    AC_MSG_RESULT(yes)
  ])

