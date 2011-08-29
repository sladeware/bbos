/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/config.h
 * @brief BB configuration header file

 BB application and library implementations access configuration macros via
 @c \#include <bb/config.h>.

 @par BB User Settable Options

 There are some configuration-options that represent user choices, rather than
 compiler defects or platform specific options. These are listed in @c <bb.h>
 header and have @c BB_CONFIG_ prefix.

 <table>
 <tr>
 <th valign="top" align="center"><b>Macro</b></th>
 <th valign="top" align="center"><b>Description</b></th>
 </tr>
 <tr>
 <td>@c BB_CONFIG_COMPILER_H</td>
 <td>Points to the name of the compiler configuration file to use. Defining
 this cuts out the compiler selection logic, and eliminates the dependency on
 the header containing that logic. For example if you are using Catalina
 compiler, then you could define @c BB_CONFIG_COMPILER_H to @c
 \"bb/builder/compilers/catalina.h\".</td>
 </tr>
 <tr>
 <td>@c BB_CONFIG_PLATFORM_H</td>
 <td>Points to the name of the platform configuration file to use. Defining
 this cuts out the platform selection logic, and eliminates the dependency on
 the header containing that logic. For example if yo are compiling on linux,
 then you could define @c BB_CONFIG_PLATFORM_H to @c
 \"bb/builder/platforms/linux.h\"</td>
 </tr>
 <tr>
 <td>@c BB_CONFIG_OS_H</td>
 <td>Points to the name of the BBOS configuration file to use. By default
 equals to @c \"bbos.h\".</td>
 </tr>
 </table>

 @par BB Macros that describe optional features

 The macro is only required if the feature is present.

 <table>
 <tr>
 <th valign="top" align="center">Macro</th>
 <th valign="top" align="center">Description</th>
 </tr>
 <tr>
 <td>@c BB_HAS_STDINT_H</td>
 <td>Defined if @c <stdint.h> header file is present.</td>
 </tr>
 <tr>
 <td>@c BB_HAS_LONG_LONG</td>
 <td>Defined if compiler supports @c long @c long data type.</td>
 </tr>
 </table>

 @par BB Information Macros

 The following macros describe bbos features.

 <table>
 <tr>
 <th valign="top" align="center"><b>Macro</b></th>
 <th valign="top" align="center"><b>Description</b></th>
 </tr>
 <tr><td colspan="2"><b>Me</b></td></tr>
 <tr>
   <td>@c BBOS_ME</td>
   <td>A string that describes who compile this OS image.</td>
 </tr>
 <tr><td colspan="2"><b>Compiler</b></td></tr>
 <tr>
 <td>@c BB_COMPILER_STR</td>
 <td>Defined as a string describing the name (and possible version) of the
 compiler in use.</td>
 </tr>
 <tr>
 <td>@c BB_COMPILER_VERSION</td>
 <td>Defined as a number describing the version of the
 compiler in use.</td>
 </tr>
 <tr>
 <td>@c BB_COMPILER_ANSIC_COMPLIANT</td>
 <td>Defines whether ANSI C Standard is supported.</td>
 </tr>
 <tr><td colspan="2"><b>Platform</b></td></tr>
 <tr>
 <td>@c BB_PLATFORM_STR</td>
 <td>Defined as a string describing the name of the platform.</td>
 </tr>
 </table>

 */

#ifndef __BB_CONFIG_H
#define __BB_CONFIG_H

/**************************
 * SELECT COMPILER CONFIG *
 **************************/

/* if we don't have a compiler config set, try and find one: */
#if !defined(BB_CONFIG_COMPILER_H)
# include "bb/builder/compilers/ccompiler.h"
#endif /* BB_CONFIG_COMPILER_H */
/* if compiler config header file was defined, include it now: */
#ifdef BB_CONFIG_COMPILER_H
# include BB_CONFIG_COMPILER_H
#else
# error "Unknown compiler"
#endif /* BB_CONFIG_COMPILER_H */

/**************************
 * SELECT PLATFORM CONFIG *
 **************************/

/* Locate which platform we are using and define BB_CONFIG_PLATFORM_H
 macro. If we do not have a platform config set, then try to find one. */
#if !defined(BB_CONFIG_PLATFORM_H)

# if defined(linux) || defined(__linux) || defined(__linux__)
#   define BB_CONFIG_PLATFORM_H "bb/builder/platforms/linux.h"
# endif

#endif /* !defined(BB_CONFIG_PLATFORM_H) */

#ifdef BB_CONFIG_PLATFORM_H
# include BB_CONFIG_PLATFORM_H
#else
# error "Unknown platform"
#endif

#ifndef BB_CONFIG_OS_H
# define BB_CONFIG_OS_H "bbos.h"
#endif

#include <bb/types.h>
#include <bb/const.h>

#endif /* __BB_CONFIG */
