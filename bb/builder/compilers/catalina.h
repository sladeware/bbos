/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file catalina.h
 * @brief Catalina compiler setup
 *
 * Catalina is ANSI C compliant (C89, with some C99 features) and so defines
 * @c BB_COMPILER_ANSIC_COMPLIANT macro.
 * See manual for more details.
 */

#define BB_COMPILER_ANSIC_COMPLIANT
#include <bb/builder/compilers/ansic.h>

#ifndef BB_COMPILER_STR
#define BB_COMPILER_STR "Catalina"
#endif
