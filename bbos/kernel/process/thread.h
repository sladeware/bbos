/*
 * Thread.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_THREAD_H
#define __BBOS_THREAD_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Number of application threads. Assume as 0 unless it was defined.
 */
#ifndef BBOS_NUMBER_OF_APPLICATION_THREADS
#define BBOS_NUMBER_OF_APPLICATION_THREADS 0
#endif /* BBOS_NUMBER_OF_APPLICATION_THREADS */

/*
 * Number of system threads, where the system threads are:
 * idle thread.
 */
#define BBOS_NUMBER_OF_SYSTEM_THREADS 2

/*
 * Some well known system thread id's.
 */
#define BBOS_IDLE_ID (BBOS_NUMBER_OF_APPLICATION_THREADS + 0)
#define BBOS_MAIN_ID (BBOS_NUMBER_OF_APPLICATION_THREADS + 1)

/*
 * Total number of threads equals to number of application threads plus
 * number of system threads.
 */
#define BBOS_NUMBER_OF_THREADS (BBOS_NUMBER_OF_APPLICATION_THREADS + BBOS_NUMBER_OF_SYSTEM_THREADS)

/*
 * Some well known thread id's.
 */
#define BBOS_IDLE_THREAD_ID (BBOS_NUMBER_OF_APPLICATION_THREADS + 0)

/* Thread management structure */
struct bbos_thread {
  bbos_thread_id_t id;
  void (*action)();
};

/* The type of the thread management structure. */
typedef struct bbos_thread bbos_thread_t;

/*
 * The number of threads should be greater than 0, but
 * less than BBOS_MAX_NUMBER_OF_THREADS.
 */
#if BBOS_NUMBER_OF_THREADS == 0
#error "BBOS_NUMBER_OF_THREADS must be >0"
#endif /* BBOS_NUMBER_OF_THREADS == 0 */
#if BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS
#error "BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS"
#endif /* BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS */

extern bbos_thread_t bbos_thread_table[BBOS_NUMBER_OF_THREADS];

/* Prototypes */

bbos_return_t bbos_thread_init(bbos_thread_id_t id, void *action);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_KERNEL_THREAD_H */

