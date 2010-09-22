/*
 * Scheduler.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/* Thread after the current thread. */
bbos_thread_id_t bbos_sched_pending;

/* Keeps current running thread identifier. */
bbos_thread_id_t bbos_sched_myself;

/**
 * bbos_sched_init - Initializes the BBOS scheduler.
 */
void
bbos_sched_init()
{
  /* Now switch to idle to start the other guys */
  bbos_sched_myself = bbos_sched_pending = BBOS_IDLE_THREAD_ID;
}

/**
 * bbos_sched_loop - Scheduling loop.
 *
 * Description:
 *
 * Should be never return.
 */
void
bbos_sched_loop()
{
  /* Scheduling loop */
  while(1) {
    /* Try to schedule next thread */
    if(bbos_sched_next() != BBOS_SUCCESS) {
      break;
    }
  }

	bbos_panic("Scheduling terminated.\n");
}

/**
 * bbos_sched_next - Schedule next thread.
 *
 * Return value:
 *
 * Generic error codes apply.
 */
bbos_return_t
bbos_sched_next()
{
  bbos_return_t err;

  bbos_sched_pending = bbos_process_thread_table[bbos_sched_myself].next;

  err = bbos_thread_switch(bbos_sched_myself);

  /* Read pending thread and set the next thread */
  bbos_sched_myself = bbos_sched_pending;

  return err;
}
