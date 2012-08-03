/*
 * Main Bionic Bunny config
 *
 * Copyright (c) 2012 Sladeware LLC
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

// If we do not have compiler config set, try and find one
#if !defined(BBOS_CONFIG_COMPILER_H)
#include "bb/config/compiler.h"
#endif // BB_CONFIG_COMPILER_H
// If compiler config header file was defined, include it now or
//  provide an error.
#ifdef BB_CONFIG_COMPILER_H
#include BB_CONFIG_COMPILER_H
#else
#error "Unknown compiler"
#endif // BB_CONFIG_COMPILER_H

// Locate which host platform we are using and define BB_CONFIG_PLATFORM_H
// macro. If we do not have a platform config set, then try to find one.
#if !defined(BB_CONFIG_PLATFORM_H)
#include "bb/config/platform.h"
#endif // !defined(BB_CONFIG_PLATFORM_H)
// If platform config header file was defined then include it now or provide an
// error.
#ifdef BB_CONFIG_PLATFORM_H
#include BB_CONFIG_PLATFORM_H
#else
#error "Unknown platform"
#endif // BB_CONFIG_PLATFORM_H

// Bionic Bunny OS specific configuration file.
#ifndef BB_CONFIG_OS_H
#warning "BB_CONFIG_OS_H wasn't defined"
#endif

// Include BB specific data types
#include <bb/types.h>
#include <bb/config/stdlib/stdint.h> // MUST be second

// Include some magic tricks
#include <bb/lib/utils/tricks.h>

#endif // __BB_CONFIG_H
