/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_SYSTEM_H
#define __BBOS_SYSTEM_H

/**
 * @file system.h
 * @brief System control
 * @ingroup bbos_kernel
 */

/* We must include stdarg.h before stdio.h. */
#include <stdarg.h>

/*
 * CAUTION:  Build setups should ensure that NDEBUG is defined on the
 * compiler command line when building bbos in release mode; else
 * assert() calls won't be removed.
 */
#include <assert.h>

/* Prototypes */

PROTOTYPE(void bbos_init, (void));
PROTOTYPE(bbos_error_t bbos_start, (void));
PROTOTYPE(void bbos_idle, (void));
PROTOTYPE(void bbos_panic, (const char* fmt, ...));

/* Thread management */
PROTOTYPE(bbos_error_t bbos_add_thread, (bbos_thread_id_t tid,
                                         void (* thread)(void)));
PROTOTYPE(bbos_error_t bbos_remove_thread, (bbos_thread_id_t tid));
PROTOTYPE(void bbos_thread_init, (bbos_thread_id_t tid, bbos_thread_t thread));
PROTOTYPE(void bbos_thread_run, (bbos_thread_id_t tid));

/* Ports */
PROTOTYPE(bbos_error_t bbos_port_send, (bbos_thread_id_t receiver,
                                        bbos_message_t* message));
PROTOTYPE(bbos_error_t bbos_port_receive, (bbos_thread_id_t tid,
                                           bbos_message_t* message));
PROTOTYPE(void bbos_port_flush, (bbos_thread_id_t tid));
PROTOTYPE(bbos_message_number_t bbos_port_is_empty, (bbos_thread_id_t tid));

#endif /* __BBOS_SYSTEM_H */
