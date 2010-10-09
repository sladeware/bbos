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
 * bbos_thread_init - Initialize thread.
 */
bbos_return_t
bbos_thread_init(bbos_thread_id_t id)
{
  bbos_thread_table[id].id = id;
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


