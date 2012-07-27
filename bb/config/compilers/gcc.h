/*
 * GNU C++ compiler support
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/config/compilers/ansic.h>

#define BB_HAS_LONG_LONG

#ifndef BB_COMPILER_NAME
# define BB_COMPILER_NAME "GNU C++ version " __VERSION__
#endif
