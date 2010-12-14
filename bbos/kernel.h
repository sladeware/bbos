/*
 * Kernel.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

/* The following are so basic, all the *.c files get them automatically. */

#include <bbos/config.h> /* MUST be first */

#define __BBOS_KERNEL__ /* Tell to everyone that this is the kernel */

/* We must include stdarg.h before stdio.h. */
#include <stdarg.h>

#include <bbos/kernel/version.h>
#include <bbos/kernel/codes.h>
#include <bbos/kernel/debug.h>
#include <bbos/kernel/types.h>

/*
 * CAUTION:  Build setups should ensure that NDEBUG is defined on the
 * compiler command line when building bbos in release mode; else
 * assert() calls won't be removed.
 */
#include <assert.h>

/* Math */
#include <bbos/kernel/math.h>

/* Timing control management */
#include <bbos/kernel/time.h>

/* When the scheduler is not disabled */
#if !defined(BBOS_DISABLE_SCHEDULER)
#include <bbos/kernel/idle.h>
#include <bbos/kernel/select_scheduler.h>
#endif

/* System management */
#include <bbos/kernel/system.h>

#endif /* __BBOS_KERNEL_H */


