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

/**
 * bbos_thread_init - Initialize thread.
 */
bbos_return_t
bbos_thread_init(bbos_thread_id_t id, void *action)
{
  bbos_thread_table[id].id = id;
  bbos_thread_table[id].action = action;
}

#endif /* BBOS_NUMBER_OF_THREADS > 0 */

