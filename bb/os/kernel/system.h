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

/**
 * Table of threads of size @c BBOS_NR_THREADS.
 */
EXTERN bbos_thread_t bbos_thread_table[BBOS_NR_THREADS];

/**
 * @def bbos_switch_thread()
 * @brief Switch to the next thread.
 * @see bbos_thread_start()
 */
#define bbos_switch_thread()                                   \
  do {                                                         \
    assert(bbos_sched_identify() < BBOS_NR_THREADS);           \
    bbos_thread_start( bbos_sched_identify() );                \
  } while (0)

/**
 * Return access to the thread's context. This feature is similar to
 * @c get_running_thread() function from @c bb.os.kernel package of
 * meta-os.
 * @see bbos_sched_identify()
 */
#define bbos_get_running_thread()               \
  bbos_thread_table[ bbos_sched_identify() ]

PROTOTYPE(bbos_error_t bbos_add_thread, (bbos_thread_id_t tid,
                                         void (* thread)(void),
                                         void* mp));
PROTOTYPE(bbos_error_t bbos_remove_thread, (bbos_thread_id_t tid));
PROTOTYPE(void bbos_thread_init, (bbos_thread_id_t tid,
                                  bbos_thread_target_t thread, void* mp));
PROTOTYPE(void bbos_thread_start, (bbos_thread_id_t tid));

/* Message-passing */

PROTOTYPE(bbos_message_t* bbos_alloc_message, ());
PROTOTYPE(void bbos_free_message, (bbos_message_t* message));
PROTOTYPE(bbos_error_t bbos_send_message, (bbos_thread_id_t receiver,
                                           bbos_message_t* message));
PROTOTYPE(bbos_error_t bbos_receive_message, (bbos_message_t** message));

#endif /* __BBOS_SYSTEM_H */
