/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_PORTABLE_STDDEF_H
#define __BBOS_LIB_PORTABLE_STDDEF_H

#include <bbos/compiler.h>

#ifndef NULL
#if defined(__cplusplus)
#define NULL (0)
#else
#define NULL ((void *)0)
#endif /* __cplusplus */
#endif /* NULL */

#endif /* __BBOS_LIB_PORTABLE_STDDEF_H */


