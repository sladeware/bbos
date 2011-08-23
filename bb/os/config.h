/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/**
 * @file config.h
 * @brief BBOS config
 * @defgroup bbos_config Config
 * @ingroup bbos_config
 */

#include <bbos.h> /* MUST be first */

#include <bb/os/version.h>
#include <bb/os/types.h>

/* if we don't have a compiler config set, try and find one: */
#if !defined(BB_COMPILER_CONFIG_H)
#include <bb/builder/compilers/ccompiler.h> /* MUST be second */
#endif /* BB_COMPILER_CONFIG_H */
/* if compiler config header file was defined, include it now: */
#ifdef BB_COMPILER_CONFIG_H
#include BB_COMPILER_CONFIG_H
#endif /* BB_COMPILER_CONFIG_H */

/**
 * @def BBOS_DEBUG
 * @brief The BBOS debug macro equals to the ANSI standard @c NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#ifndef BBOS_DEBUG
#define BBOS_DEBUG NDEBUG
#endif

/**
 * @name System
 * @{
 */

#ifndef BBOS_NR_THREADS
#error "Please define BBOS_NR_THREADS in <bbos.h>"
#endif

/** @} */

/**
 * @name Hardware
 * @{
 */

#ifndef BBOS_PROCESSOR_NAME
#error "BBOS_PROCESSOR_NAME was not defined"
#endif

/**
 * @def BBOS_PROCESSOR_FILE(filename)
 * @brief Build path for the proper processor.
 */
#define BBOS_PROCESSOR_FILE(filename)                   \
  <bb/os/hardware/processors/BBOS_PROCESSOR/filename>

/** @} */

/**
 * Banner.
 */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR \
  " (" BB_COMPILER_STR ")" "\n";

#endif /* __BBOS_CONFIG_H */
