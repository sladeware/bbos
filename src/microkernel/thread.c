/*
 * The BBOS thread is an independent context within a process. All the threads
 * are determined at compile time and can be start and stopped at runtime, but
 * cannot be created or destroyed.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/microkernel/thread.h>
#include <bbos/microkernel/process.h>

/**
 * bbos_thread_get_priority - Get the target thread's priority.
 * @tid: Thread identifier.
 */
bbos_thread_priority_t
bbos_thread_get_priority(bbos_thread_id_t tid)
{
  assert(tid < BBOS_NUMBER_OF_THREADS);
  return bbos_process_thread_table[tid].priority;
}

/**
 * bbos_thread_set_priority - Set the target thread's priority.
 * @tid: Thread identifier.
 * @prio: Thread priority.
 */
void
bbos_thread_set_priority(bbos_thread_id_t tid, bbos_thread_priority_t prio)
{
  assert(tid < BBOS_NUMBER_OF_THREADS); // check thread id

  bbos_process_thread_table[tid].priority = prio;
}

/**
 * bbos_thread_start - Put the thread into the list of ready threads.
 * @tid: Thread identifier.
 *
 * Note:
 *
 * The thread will be added to the end of list.
 *
 * Return value:
 *
 * Generic error codes.
 */
bbos_return_t
bbos_thread_start(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  if(bbos_process_thread_table[tid].next != BBOS_IDLE_ID) {
    /* Sorry, but that thread is ready! */
    return BBOS_FAILURE;
  }

  if (bbos_process_thread_table[BBOS_IDLE_ID].next == BBOS_IDLE_ID) {
    bbos_process_thread_table[BBOS_IDLE_ID].next = tid;
  }
  else {
    bbos_process_thread_table[bbos_process_thread_table[BBOS_IDLE_ID].prev].next = tid;
  }

  bbos_process_thread_table[tid].next = bbos_process_thread_table[BBOS_IDLE_ID].next;
  bbos_process_thread_table[tid].prev = bbos_process_thread_table[BBOS_IDLE_ID].prev;
  bbos_process_thread_table[BBOS_IDLE_ID].prev = tid;

  return BBOS_SUCCESS;
}

/**
 * bbos_thread_stop - Stop the target thread.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Generic error codes.
 */
bbos_return_t
bbos_thread_stop(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  /* Thread is stopped already */
  if(bbos_process_thread_table[tid].next == BBOS_IDLE_ID) {
    return BBOS_FAILURE;
  }

  /* In the case when the scheduler consits of only one tread */
  if(((bbos_process_thread_table[BBOS_IDLE_ID].next - tid) | (tid - bbos_process_thread_table[BBOS_IDLE_ID].prev)) == 0) {
    bbos_process_thread_table[BBOS_IDLE_ID].next = BBOS_IDLE_ID;
    bbos_process_thread_table[BBOS_IDLE_ID].prev = BBOS_IDLE_ID;
  }
  else if(bbos_process_thread_table[BBOS_IDLE_ID].next == tid) {
    bbos_process_thread_table[BBOS_IDLE_ID].next = bbos_process_thread_table[tid].next;
    bbos_process_thread_table[bbos_process_thread_table[BBOS_IDLE_ID].next].prev = bbos_process_thread_table[BBOS_IDLE_ID].prev;
  }
  else if (bbos_process_thread_table[BBOS_IDLE_ID].prev == tid) {
    bbos_process_thread_table[BBOS_IDLE_ID].prev = bbos_process_thread_table[tid].prev;
    bbos_process_thread_table[bbos_process_thread_table[BBOS_IDLE_ID].prev].next = bbos_process_thread_table[BBOS_IDLE_ID].next;
  }
  else {
    bbos_process_thread_table[bbos_process_thread_table[tid].prev].next = bbos_process_thread_table[tid].next;
    bbos_process_thread_table[bbos_process_thread_table[tid].next].prev = bbos_process_thread_table[tid].prev;
  }

  bbos_process_thread_table[tid].next = BBOS_IDLE_ID;
  bbos_process_thread_table[tid].prev = BBOS_IDLE_ID;

  if(((bbos_process_thread_table[BBOS_IDLE_ID].next - BBOS_IDLE_ID) | (bbos_process_thread_table[BBOS_IDLE_ID].prev - BBOS_IDLE_ID)) == 0) {
    bbos_process_thread_table[BBOS_IDLE_ID].next = BBOS_IDLE_ID;
  }

  return BBOS_SUCCESS;
}

