/*
 * GNU C++ compiler support
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */
#ifndef __BB_CONFIG_COMPILERS_GCC_H
#define __BB_CONFIG_COMPILERS_GCC_H

#include <bb/config/compilers/ansic.h>

#define BB_HAS_LONG_LONG

#ifndef BB_COMPILER_NAME
#define BB_COMPILER_NAME "GNU C++ version " __VERSION__
#endif

#endif /* __BB_CONFIG_COMPILERS_GCC_H */
