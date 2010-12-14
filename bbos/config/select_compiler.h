/*
 * Compiler configuration selection.
 * 
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
 
/* 
 * Determine which compiler we are using and define BBOS_COMPILER_CONFIG_FILE 
 * as required.
 */
 
#if defined(__GNUC__)
#	define BBOS_COMPILER_CONFIG_FILE <bbos/config/compilers/gcc.h>
#elif defined __CATALINA__
#	define BBOS_COMPILER_CONFIG_FILE <bbos/config/compilers/catalina.h>
#else
// The compiler was not recognized. Generate an error.
#	error "Unknown compiler. Please provide the config file."
#endif

// Set default values
#ifndef BBOS_COMPILER
#	define BBOS_COMPILER "Unknown Compiler"
#endif


