/*
 * Main BB config
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BB_CONFIG_H
#define __BB_CONFIG_H

/* If we do not have compiler config set, try and find one */
#if !defined(BBOS_CONFIG_COMPILER_H)
# include "bb/config/compiler.h"
#endif /* BB_CONFIG_COMPILER_H */
/* If compiler config header file was defined, include it now or provide an
   error. */
#ifdef BB_CONFIG_COMPILER_H
# include BB_CONFIG_COMPILER_H
#else
# error "Unknown compiler"
#endif /* BB_CONFIG_COMPILER_H */

/* Locate which platform we are using and define BB_CONFIG_PLATFORM_H macro.
 If we do not have a platform config set, then try to find one. */
#if !defined(BB_CONFIG_PLATFORM_H)
# include "bb/config/platform.h"
#endif /* !defined(BB_CONFIG_PLATFORM_H) */
/* If platform config header file was defined then include it now ot provide
   an error. */
#ifdef BB_CONFIG_PLATFORM_H
# include BB_CONFIG_PLATFORM_H
#else
# error "Unknown platform"
#endif /* BB_CONFIG_PLATFORM_H */

#ifndef BB_CONFIG_OS_H
# define BB_CONFIG_OS_H <bbos_config.h>
#endif

#include <bb/types.h> /* include BB specific data types */

#include <bb/utils/tricks.h> /* include some magic tricks */

#endif /* __BB_CONFIG_H */