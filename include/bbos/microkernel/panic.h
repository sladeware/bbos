/*
 * Panic handling.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_PANIC_H
#define __BBOS_MICROKERNEL_PANIC_H

#include <bbos/lib/stdarg.h>
#include <bbos/lib/stdio.h>
#include <bbos/env.h>

/* Prototypes */

void bbos_panic(const char *fmt, ...);

#endif /* __BBOS_MICROKERNEL_PANIC_H */

