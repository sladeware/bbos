/*
 * Main Bionic Bunny config.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
#ifndef __BB_CONFIG_H
#define __BB_CONFIG_H

/* Check compiler config set, try and find one. */
#if !defined(BBOS_CONFIG_COMPILER_H)
#include "bb/config/compiler.h"
#endif /* BB_CONFIG_COMPILER_H */
/* Include compiler config header file or provide an error. */
#ifdef BB_CONFIG_COMPILER_H
#include BB_CONFIG_COMPILER_H
#else
#error "Unknown compiler"
#endif /* BB_CONFIG_COMPILER_H */

/*
 * Locate which host platform we are using and define BB_CONFIG_PLATFORM_H
 * macro. If we do not have a platform config set, then try to find one.
 */
#if !defined(BB_CONFIG_HOST_PLATFORM_H)
#include "bb/config/host_platform.h"
#endif /* !defined(BB_CONFIG_HOST_PLATFORM_H) */
/* Check platform config header file or provide an error. */
#ifdef BB_CONFIG_HOST_PLATFORM_H
#include BB_CONFIG_HOST_PLATFORM_H
#else
#error "Unknown host platform"
#endif /* BB_CONFIG_HOST_PLATFORM_H */

/* Include some magic tricks */
#include <bb/lib/utils/tricks.h>

/*
 * Makes path to compiler's standard library file. Please use this macro,
 * instead of directly include these files.
 */
#define BB_STDLIB_FILE(file)                    \
  BB_STR(BB_PATH_JOIN2(bb/config/stdlib, file))

#include BB_STDLIB_FILE(stdint.h)

/* Integer constant 0. Used for turning integers into booleans. */
#define BB_FALSE 0
/* Integer constant !FALSE or 1. Used for turning integers to booleans. */
#define BB_TRUE !(BB_FALSE)

#endif /* __BB_CONFIG_H */
