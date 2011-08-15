/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/**
 * @file config.h
 * @brief BBOS config
 */

/* Always goes first */
#include <bbos.h>

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

#endif
