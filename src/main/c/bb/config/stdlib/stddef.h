/*
 * <stddef.h> header file wrapper
 *
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __BB_STDDEF_H
#define __BB_STDDEF_H

#include <stddef.h>

#ifndef _SIZE_T
#define _SIZE_T
/* The type size_t holds all results of the sizeof operator. At first glance,
   it seems obvious that it should be an unsigned int, but this is not always
   the case. */
typedef unsigned int size_t; /* type returned by sizeof */
#endif

#ifndef _SSIZE_T
#define _SSIZE_T
typedef int ssize_t; /* signed version of size_t */
#endif

#endif /* __BB_STDDEF_H */
