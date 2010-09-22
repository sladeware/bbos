/*
 * Thread.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_THREAD_H
#define __BBOS_THREAD_H

#ifdef __cplusplus
extern "C" {
#endif

/* 
 * Release the processor non-preemtively.
 */
#ifndef bbos_thread_switch
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

/*
 * Number of system threads, where the system threads are:
 * idle thread.
 */
#define BBOS_NUMBER_OF_SYSTEM_THREADS 1

/*
 * Number of config threads. Assume as 0 unless it was defined.
 */
#ifndef BBOS_NUMBER_OF_CONFIG_THREADS
#define BBOS_NUMBER_OF_CONFIG_THREADS 0
#endif /* BBOS_NUMBER_OF_CONFIG_THREADS */

/*
 * Total number of threads equals to number of config threads plus
 * number of system threads.
 */
#define BBOS_NUMBER_OF_THREADS						\
  (BBOS_NUMBER_OF_CONFIG_THREADS + BBOS_NUMBER_OF_SYSTEM_THREADS)

/*
 * Some well known thread id's.
 */
#define BBOS_IDLE_THREAD_ID (BBOS_NUMBER_OF_CONFIG_THREADS + 0)

/*
 * Some well known thread priorities.
 */
#define BBOS_THREAD_LOWEST_PRIORITY (BBOS_THREAD_MAX_PRIORITY_VALUE)
#define BBOS_IDLE_THREAD_PRIORITY BBOS_THREAD_LOWEST_PRIORITY

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

/* Well known idle thread structure */
#define bbos_idle_thread (bbos_thread_table[BBOS_IDLE_THREAD_ID])

/* Prototypes */

bbos_return_t bbos_thread_init(bbos_thread_id_t tid, 
  bbos_thread_priority_t prio);

bbos_thread_priority_t bbos_thread_get_priority(bbos_thread_id_t tid);

void bbos_thread_set_priority(bbos_thread_id_t tid, bbos_thread_priority_t prio);

bbos_return_t bbos_thread_resume(bbos_thread_id_t tid);

bbos_return_t bbos_thread_suspend(bbos_thread_id_t tid);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_KERNEL_THREAD_H */

