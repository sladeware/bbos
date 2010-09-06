/*
 * Kernel.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
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

#include <bbos/kernel/time.h>

#include <bbos/kernel/mm.h>

/* Data types. */
#include <bbos/kernel/list.h>
#include <bbos/kernel/queue.h>

#include <bbos/kernel/hardware.h>
#include <bbos/kernel/process.h>
#include <bbos/kernel/itc.h>
#include <bbos/kernel/system.h>

#endif /* __BBOS_KERNEL_H */

