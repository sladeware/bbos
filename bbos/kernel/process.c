/*
 * Process.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/**
 * bbos_process_init - Initialize process.
 *
 * Description:
 *
 * The process initialization includes: scheduler initialization, threads 
 * initialization and inter-thread communication initialization.
 */
void
bbos_process_init()
{
  int id;

  printf("Initialize process\n");

#if BBOS_NUMBER_OF_PORTS > 0
  /* Initialize ports */
  for (id=0; id<BBOS_NUMBER_OF_PORTS; id++) {
    bbos_port_init(id, NULL, 0);
  }
#endif

#if BBOS_NUMBER_OF_MEMPOOLS > 0
  /* Initialize memory pools */
  for (id=0; id<BBOS_NUMBER_OF_MEMPOOLS; id++) {
    bbos_mempool_init(id, NULL, 0, 0);
  }
#endif

  /* Initialize scheduler */
  bbos_scheduler_init();

  /* Initialize threads */
  for (id=0; id<BBOS_NUMBER_OF_THREADS; id++) {
    bbos_thread_init(id, NULL);
  }

  bbos_thread_init(BBOS_IDLE_ID, bbos_idle);
	bbos_thread_init(BBOS_MAIN_ID, bbos_main);

  bbos_scheduler_insert_thread(BBOS_IDLE_ID);
	bbos_scheduler_insert_thread(BBOS_MAIN_ID);
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
	printf("Start process\n");

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

