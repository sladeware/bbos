/*
 * The BBOS thread is an independent context within a process. All the threads
 * are determined at compile time and can be start and stopped at runtime, but
 * cannot be created or destroyed.
 *
 * Basically we say that thread is subprocess created by a parent process.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/*
 * At least one thread should always exist, which means BBOS_NUMBER_OF_THREADS 
 * always > 0. Just a test.
 */
#if BBOS_NUMBER_OF_THREADS > 0

struct bbos_thread bbos_thread_table[BBOS_NUMBER_OF_THREADS];

#endif /* BBOS_NUMBER_OF_THREADS > 0 */

/**
 * bbos_thread_get_priority - Get thread's priority.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Priority value.
 */
bbos_thread_priority_t
bbos_thread_get_priority(bbos_thread_id_t tid)
{
  assert(tid < BBOS_NUMBER_OF_THREADS);

  return bbos_thread_table[tid].priority;
}

/**
 * bbos_thread_set_priority - Set thread's priority.
 * @tid: Thread identifier.
 * @prio: Thread priority.
 */
void
bbos_thread_set_priority(bbos_thread_id_t tid, bbos_thread_priority_t prio)
{
  assert(tid < BBOS_NUMBER_OF_THREADS); // check thread id

  bbos_thread_table[tid].priority = prio;
}

/**
 * bbos_thread_init
 *
 * Description:
 *
 * Initialize thread and put it into the list of ready threads for scheduler.
 */
bbos_return_t
bbos_thread_init(bbos_thread_id_t tid, bbos_thread_priority_t prio)
{
  bbos_thread_set_priority(tid, prio);

  bbos_scheduler_insert_thread(tid);
}

/**
 * bbos_thread_suspend - Suspend thread.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_thread_suspend(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  return bbos_scheduler_suspend_thread(tid);
}

/**
 * bbos_thread_resume - Resume thread activity.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_thread_resume(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  return bbos_scheduler_resume_thread(tid);
}

bbos_return_t
bbos_thread_destroy(bbos_thread_id_t tid)
{
  return bbos_scheduler_remove_thread(tid);
}


