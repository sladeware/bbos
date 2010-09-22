/*
 * The basic scheduler is a simple contant time approach that maintains a 
 * double-linked list of running threads.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

bbos_thread_id_t current_thread;
bbos_thread_id_t pending_thread;

struct schedule_record {
  bbos_thread_id_t next;
  bbos_thread_id_t prev;
};

/* Double-linked list of running threads. */
struct schedule_record schedule[BBOS_NUMBER_OF_THREADS];

/**
 * bbos_sched_insert_thread - Put the thread into the list of ready threads.
 * @tid: Thread identifier.
 *
 * Note:
 *
 * The thread will be added to the end of list.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_scheduler_insert_thread(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  if(schedule[tid].next != BBOS_IDLE_THREAD_ID) {
    /* Sorry, but that thread is ready! */
    return BBOS_FAILURE;
  }

  if (schedule[BBOS_IDLE_THREAD_ID].next == BBOS_IDLE_THREAD_ID) {
    schedule[BBOS_IDLE_THREAD_ID].next = tid;
  }
  else {
    schedule[schedule[BBOS_IDLE_THREAD_ID].prev].next = tid;
  }

  schedule[tid].next = schedule[BBOS_IDLE_THREAD_ID].next;
  schedule[tid].prev = schedule[BBOS_IDLE_THREAD_ID].prev;
  schedule[BBOS_IDLE_THREAD_ID].prev = tid;

  return BBOS_SUCCESS;
}

/**
 * bbos_scheduler_remove_thread - Remove thread from list of ready threads.
 * @tid: Thread identifier.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_scheduler_remove_thread(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  /* Thread is stopped already */
  if(schedule[tid].next == BBOS_IDLE_THREAD_ID) {
    return BBOS_FAILURE;
  }

  /* In the case when the scheduler consits of only one tread */
  if(((schedule[BBOS_IDLE_THREAD_ID].next - tid) | (tid - schedule[BBOS_IDLE_THREAD_ID].prev)) == 0) {
    schedule[BBOS_IDLE_THREAD_ID].next = BBOS_IDLE_THREAD_ID;
    schedule[BBOS_IDLE_THREAD_ID].prev = BBOS_IDLE_THREAD_ID;
  }
  else if(schedule[BBOS_IDLE_THREAD_ID].next == tid) {
    schedule[BBOS_IDLE_THREAD_ID].next = schedule[tid].next;
    schedule[schedule[BBOS_IDLE_THREAD_ID].next].prev = schedule[BBOS_IDLE_THREAD_ID].prev;
  }
  else if (bbos_idle_thread.prev == tid) {
    schedule[BBOS_IDLE_THREAD_ID].prev = schedule[tid].prev;
    schedule[schedule[BBOS_IDLE_THREAD_ID].prev].next = schedule[BBOS_IDLE_THREAD_ID].next;
  }
  else {
    schedule[schedule[tid].prev].next = schedule[tid].next;
    schedule[schedule[tid].next].prev = schedule[tid].prev;
  }

  schedule[tid].next = BBOS_IDLE_THREAD_ID;
  schedule[tid].prev = BBOS_IDLE_THREAD_ID;

  if(((schedule[BBOS_IDLE_THREAD_ID].next - BBOS_IDLE_THREAD_ID) | (schedule[BBOS_IDLE_THREAD_ID].prev - BBOS_IDLE_THREAD_ID)) == 0) {
    schedule[BBOS_IDLE_THREAD_ID].next = BBOS_IDLE_THREAD_ID;
  }

  return BBOS_SUCCESS;
}

/**
 * bbos_sched_init - Initializes the BBOS scheduler.
 */
void
bbos_scheduler_init()
{
  /* Now switch to idle to start the other guys */
  current_thread = pending_thread = BBOS_IDLE_THREAD_ID;
}

/**
 * bbos_scheduler_get_next_thread - Returns next thread for switching.
 *
 * Return value:
 *
 * Thread identifier.
 */
bbos_thread_id_t
bbos_scheduler_get_next_thread()
{
  /* Read pending thread and set the next thread */
  current_thread = pending_thread;

  pending_thread = schedule[current_thread].next;

  return current_thread;
}

/**
 * bbos_sched_identify_thread - Identifies running thread.
 *
 * Return value:
 *
 * Thread identifier.
 */
bbos_thread_id_t
bbos_scheduler_identify_thread()
{
  return current_thread;
}

