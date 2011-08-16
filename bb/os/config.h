/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/**
 * @file config.h
 * @brief BBOS config
 */

#include <bbos.h> /* MUST be first */

#include <bb/os/version.h>

/* if we don't have a compiler config set, try and find one: */
#if !defined(BB_COMPILER_CONFIG_H)
#include <bb/builder/compilers/ccompiler.h> /* MUST be second */
#endif /* BB_COMPILER_CONFIG_H */
/* if compiler config header file was defined, include it now: */
#ifdef BB_COMPILER_CONFIG_H
#include BB_COMPILER_CONFIG_H
#endif /* BB_COMPILER_CONFIG_H */

#ifndef BBOS_NUM_THREADS
#error "Please define BBOS_NUM_THREADS in <bbos.h>"
#endif

#ifndef BBOS_DEBUG
/**
 * The BBOS debug macro equals to the ANSI standard NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#define BBOS_DEBUG NDEBUG
#endif

/* Hardware */
#ifndef BBOS_PROCESSOR
#error "BBOS_PROCESSOR was not defined"
#endif
#define BBOS_FIND_PROCESSOR_FILE(filename) <bb/os/hardware/processors/BBOS_PROCESSOR/filename>

/* Banner */
const char bbos_banner[] = "BBOS version " BBOS_VERSION_STR "\n";

#endif
