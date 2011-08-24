/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file gcc.h
 * @brief GNU C++ compiler setup
 */

#include <bb/builder/compilers/ansic.h>

#define BB_HAS_LONG_LONG

#ifndef BB_COMPILER_STR
#define BB_COMPILER_STR "GNU C++ version " __VERSION__
#endif