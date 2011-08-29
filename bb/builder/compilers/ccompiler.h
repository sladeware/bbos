/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file ccompiler.h
 * @brief C compiler configuration selection header file
 */

/* Detect which compiler we are using and define BB_COMPILER_CONFIG_H as 
  needed: */
#if defined(__GNUC__) /* GNU C++ */
# define BB_CONFIG_COMPILER_H "bb/builder/compilers/gcc.h"
#elif defined(__CATALINA__) /* Catalina compiler */
# define BB_CONFIG_COMPILER_H "bb/builder/compilers/catalina.h"
#else /* generate an error if compiler wasn't recognised */
# error "Unknown compiler - please report support team"
#endif
