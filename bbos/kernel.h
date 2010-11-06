/*
 * Kernel.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

#define BBOS

#include <bbos/kernel/version.h>
#include <bbos/kernel/codes.h>
#include <bbos/kernel/debug.h>
#include <bbos/kernel/types.h>

/* We must include stdarg.h before stdio.h. */
#include <stdarg.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
 * CAUTION:  Build setups should ensure that NDEBUG is defined on the
 * compiler command line when building bbos in release mode; else
 * assert() calls won't be removed.
 */
#include <assert.h>

/* Temporary header files. They will be moved soon. */
#include <bbos/compiler.h>
#include <bbos/hardware.h>

/* Math */
#include <bbos/kernel/math.h>

/* Memory management */
#include <bbos/kernel/mm.h>

/* Timing control */
#include <bbos/kernel/time.h>

/* Process management */
#include <bbos/kernel/process.h>

/* System management */
#include <bbos/kernel/system.h>

#endif /* __BBOS_KERNEL_H */


