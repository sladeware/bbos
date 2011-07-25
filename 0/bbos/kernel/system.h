/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

/**
 * @file system.h
 * @brief System control
 */

#ifndef __BBOS_SYSTEM_H
#define __BBOS_SYSTEM_H

/* We must include stdarg.h before stdio.h. */
#include <stdarg.h>

/*
 * CAUTION:  Build setups should ensure that NDEBUG is defined on the
 * compiler command line when building bbos in release mode; else
 * assert() calls won't be removed.
 */
#include <assert.h>

#include <bbos/config.h>
#include <bbos/kernel/types.h>

#ifdef BBOS_SCHED_ENABLED
#include <bbos/kernel/sched.h>
#endif

void bbos_init();
void bbos_start();
void bbos_panic(const char *fmt, ...);
bbos_error_t bbos_start_thread(bbos_thread_id_t tid, void (*thread)(void));
bbos_error_t bbos_stop_thread(bbos_thread_id_t tid);

#endif

