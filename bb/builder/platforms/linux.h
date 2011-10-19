/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/builder/platforms/linux.h
 * @brief Linux platform specific configurations
 */

#define BB_PLATFORM_STR "linux"

#if defined(__GLIBC__) \
  && ((__GLIBC__ > 2) || ((__GLIBC__ == 2) && (__GLIBC_MINOR__ >= 1)))
#  if defined __GNUC__
#    define BB_HAS_STDINT_H
#  endif
#endif
