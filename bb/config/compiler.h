//
// Copyright (c) 2011 Sladeware LLC
//
// Author: Oleksandr Sviridenko

#ifndef __BB_CONFIG_COMPILER_H
#define __BB_CONFIG_COMPILER_H

// Detect which compiler we are using and define BB_COMPILER_CONFIG_H as needed
#if defined(__GNUC__) /* GNU C++ */
# define BB_CONFIG_COMPILER_H "bb/config/compilers/gcc.h"
#elif defined(__CATALINA__) /* Catalina compiler */
# define BB_CONFIG_COMPILER_H "bb/config/compilers/catalina.h"
#else /* Generate an error if compiler wasn't recognised */
# error "Unknown compiler - please report supprt team"
#endif

#endif // __BB_CONFIG_COMPILER_H
