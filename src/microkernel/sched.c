/*
 * The scheduler.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/sched.h>
#include <bbos/microkernel/process.h>

/**
 * bbos_sched_init - Initializes the BBOS scheduler.
 */
void
bbos_sched_init()
{
  /* Now switch to idle to start the other guys */
  bbos_sched_myself = bbos_sched_pending = BBOS_IDLE_ID;
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

  bbos_sched_pending = bbos_process_thread_table[bbos_sched_myself()].next;

  err = bbos_thread_switch(bbos_sched_myself());

  /* Read pending thread and set the next thread */
  bbos_sched_myself = bbos_sched_pending;

  return err;
}
