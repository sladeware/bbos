/*
 * Panic handling.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_PANIC_H
#define __BBOS_MICROKERNEL_PANIC_H

#include <bbos/env.h>
#include <stdarg.h>
//#include <stdio.h>

/* Prototypes */

void bbos_panic(const uint8_t *fmt, ...);

#endif /* __BBOS_MICROKERNEL_PANIC_H */

