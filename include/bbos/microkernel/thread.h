/*
 * The BBOS thread.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_THREAD_H
#define __BBOS_MICROKERNEL_THREAD_H

/* Include the environment */
#include <bbos/env.h>

/**
 * bbos_thread_switch - Release the processor non-preemtively.
 */
#ifndef bbos_thread_switch
//#warning "bbos_thread_switch service is undefined"
#define bbos_thread_switch bbos_thread_dummy_switch

/**
 * bbos_thread_dummy_switch - Dummy thread switcher.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Always returns BBOS_SUCCESS code.
 */
static bbos_return_t
bbos_thread_dummy_switch(bbos_thread_id_t tid)
{
  return BBOS_SUCCESS;
}
#endif /* bbos_thread_switch */

/**
 * Number of system threads, where the system threads are:
 * idle thread.
 */
#define BBOS_NUMBER_OF_SYSTEM_THREADS 1

/**
 * Number of config threads. Will be assumed as 0 unless it was defined.
 */
#ifndef BBOS_NUMBER_OF_CONFIG_THREADS
//#warning "BBOS_NUMBER_OF_CONFIG_THREADS was not defined"
#define BBOS_NUMBER_OF_CONFIG_THREADS 0
#endif /* BBOS_NUMBER_OF_CONFIG_THREADS */

/**
 * Total number of threads equals to number of config threads plus
 * number of system threads.
 */
#define BBOS_NUMBER_OF_THREADS						\
  (BBOS_NUMBER_OF_CONFIG_THREADS + BBOS_NUMBER_OF_SYSTEM_THREADS)

/**
 * Some well known thread id's.
 */
#define BBOS_IDLE_ID (BBOS_NUMBER_OF_CONFIG_THREADS + 0)

/**
 * Some well known thread priorities.
 */
#define BBOS_THREAD_LOWEST_PRIORITY (BBOS_THREAD_MAX_PRIORITY_VALUE)
#define BBOS_IDLE_PRIO BBOS_THREAD_LOWEST_PRIORITY

/**
 * struct bbos_thread - The thread management structure.
 * @priority: Thread priority.
 * @next: Next thread identifier.
 * @prev: Previous thread identifier.
 */
struct bbos_thread {
  /* General fields */
  bbos_thread_priority_t priority;

  /* Scheduling fields */
  bbos_thread_id_t next;
  bbos_thread_id_t prev;
};

/** The type of the thread management structure. */
typedef struct bbos_thread bbos_thread_t;

/* Prototypes */

bbos_thread_priority_t bbos_thread_get_priority(bbos_thread_id_t tid);
void bbos_thread_set_priority(bbos_thread_id_t tid, bbos_thread_priority_t prio);

bbos_return_t bbos_thread_start(bbos_thread_id_t tid);

bbos_return_t bbos_thread_stop(bbos_thread_id_t tid);

#endif /* __BBOS_MICROKERNEL_THREAD_H */

