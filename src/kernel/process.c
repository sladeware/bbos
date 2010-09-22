/*
 * Process.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_process_init - Initialize process.
 *
 * Description:
 *
 * Initialize threads, inter-thread communication and scheduler.
 */
void
bbos_process_init()
{
  /* Initialize scheduler */
  bbos_scheduler_init();

  /* Initialize and schedule threads */
  bbos_thread_init(BBOS_IDLE_THREAD_ID, BBOS_IDLE_THREAD_PRIORITY);

  /* Initialize inter-thread communication mechanisms */
  bbos_itc_init();
}

/**
 * bbos_process_start - Start process.
 *
 * Description:
 *
 * 
 */
void
bbos_process_start()
{
  bbos_thread_id_t tid;

  while(1) {
    tid = bbos_scheduler_get_next_thread();
    bbos_thread_switch(tid);
  }
}

/**
 * bbos_process_stop - Stop process.
 */
void
bbos_process_stop()
{
}

