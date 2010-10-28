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
 * The process initialization includes: scheduler initialization, threads 
 * initialization and inter-thread communication initialization.
 *
 * Start idle thread.
 */
void
bbos_process_init()
{
  int id;

  printf("Initialize process\n");

  /* Initialize ports */
  for (id=0; id<BBOS_NUMBER_OF_PORTS; id++) {
    bbos_port_init(id, NULL, 0);
  }

  /* Initialize memory pools */
  for (id=0; id<BBOS_NUMBER_OF_MEMPOOLS; id++) {
    bbos_mempool_init(id, NULL, 0, 0);
  }

  /* Initialize scheduler */
  bbos_scheduler_init();

  /* Initialize threads */
  for (id=0; id<BBOS_NUMBER_OF_THREADS; id++) {
    bbos_thread_init(id, NULL);
  }

  bbos_thread_init(BBOS_IDLE_ID, bbos_idle);

  bbos_scheduler_insert_thread(BBOS_IDLE_ID);
}

/**
 * bbos_process_start - Start the process.
 *
 * Description:
 *
 * Uses scheduler to move by threads. Stops if has an error.
 */
void
bbos_process_start()
{
  bbos_scheduler_do_loop();

  bbos_panic("Scheduler exit.");
}

/**
 * bbos_process_stop - Stop the process.
 */
void
bbos_process_stop()
{
}

