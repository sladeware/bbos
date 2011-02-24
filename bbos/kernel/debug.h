
#ifndef __BBOS_DEBUG_H
#define __BBOS_DEBUG_H

/**
 * @file debug.h
 * @brief Debug
 */

#include <assert.h>

#ifndef BBOS_DEBUG
/**
 * The BBOS debug macro equals to the ANSI standard NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#define BBOS_DEBUG NDEBUG
#endif

#endif

