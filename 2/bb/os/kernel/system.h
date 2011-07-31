/*
 * Copyright (c) 2011 Sladeware LLC
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

#include <bb/os/config.h>
#include <bb/os/kernel/errors.h>
#include <bb/os/kernel/types.h>

#ifndef BBOS_DEBUG
/**
 * The BBOS debug macro equals to the ANSI standard NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#define BBOS_DEBUG NDEBUG
#endif

#ifdef BBOS_SCHED_ENABLED
#include <bb/os/kernel/sched.h>
#endif

void bbos_init();
void bbos_start();
void bbos_idle_runner();
void bbos_panic(const char *fmt, ...);

/* Thread management */
bbos_error_t bbos_add_thread(bbos_thread_id_t tid, void (*thread)(void));
bbos_error_t bbos_remove_thread(bbos_thread_id_t tid);
void bbos_thread_init(bbos_thread_id_t tid, bbos_thread_t thread);
void bbos_thread_run(bbos_thread_id_t tid);

/* Ports */
bbos_error_t bbos_port_send(bbos_thread_id_t receiver, bbos_message_t *message,
                            bbos_thread_id_t owner);
bbos_error_t bbos_port_receive(bbos_thread_id_t tid, bbos_message_t *message);
void bbos_port_flush(bbos_thread_id_t tid);
bbos_message_number_t bbos_port_is_empty(bbos_thread_id_t tid);

#endif

