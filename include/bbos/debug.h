/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_DEBUG_H
#define __BBOS_DEBUG_H

#include <bbos/compiler.h>

/**
 * The BBOS debug macro equals to the ANSI standard NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#define BBOS_DEBUG NDEBUG

#if defined(BBOS_DEBUG)
#define assert(x)							\
  do {									\
    if (!(x)) {								\
      printf("ASSERT(%s) failed in %s, file: %s:%d\n", #x, __FUNCTION__, __FILE__, __LINE__); \
    }									\
  } while (0)
#else
#define assert(x) do { } while (0)
#endif

#endif /* __BBOS_DEBUG_H */
