/*
 * BBOS configuration header file.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/*
 * CAUTION: The file is intended to be stable - DO NOT MODIFY THIS FILE!
 *
 * Config order:
 *
 *	BBOS_APPLICATION_CONFIG_FILE
 *	BBOS_COMPILER_CONFIG_FILE
 */

// The application config file
#if !defined(BBOS_APPLICATION_CONFIG_FILE)
#	define BBOS_APPLICATION_CONFIG_FILE <bbos.h>
#endif

// Include application config file first
#ifdef BBOS_APPLICATION_CONFIG_FILE
#	include BBOS_APPLICATION_CONFIG_FILE
#endif

// Select proper compiler config set
#if !defined(BBOS_COMPILER_CONFIG_FILE)
#	include <bbos/config/select_compiler.h>
#endif

// Include compiler config file provided by developer or selected automatically
#ifdef BBOS_COMPILER_CONFIG_FILE
#	include BBOS_COMPILER_CONFIG_FILE
#endif

#endif /* __BBOS_CONFIG_H */

