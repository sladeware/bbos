/*
 * The BBOS process.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/process.h>

/**
 * bbos_process_init_threads - Initialize threads within target process.
 *
 * Description:
 *
 * Initialize all of the threads. By default each thread doesn't support
 * ITC mechanism and it has the lowest priority defined as
 * BBOS_THREAD_LOWEST_PRIORITY.
 */
void
bbos_process_init_threads()
{
  bbos_thread_id_t tid;

  for(tid=0; tid<BBOS_NUMBER_OF_THREADS; tid++) {
    /* General */
    bbos_thread_set_priority(tid, BBOS_THREAD_LOWEST_PRIORITY);

    /* Scheduling */
    bbos_process_thread_table[tid].next = BBOS_IDLE_ID;
    bbos_process_thread_table[tid].prev = BBOS_IDLE_ID;
  }
}

/**
 * bbos_process_init_ports - Initialize ports.
 */
void
bbos_process_init_ports()
{
  bbos_port_id_t p;

  for(p=0; p<BBOS_NUMBER_OF_PORTS; p++) {
    bbos_process_port_table[p].buffer = (fastmempool_t *)NULL;
    bbos_process_port_table[p].queue = (queue_t *)NULL;
  }
}

/**
 * bbos_process_init - Initialize the current process.
 */
void
bbos_process_init()
{
  bbos_process_init_ports();
  bbos_process_init_threads();
}


