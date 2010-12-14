/*
 * The First-Come-First-Served (FCFS) scheduler is a simple contant time 
 * approach that maintains a double-linked list of running threads.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/config.h>
#include <stdio.h>
#include <bbos/schedulers/fcfs.h>
#include <assert.h>

static bbos_thread_id_t target_tid = BBOS_IDLE_ID;

struct thread {
	void (*action)();
	bbos_thread_id_t next;
	bbos_thread_id_t prev;
};

// Double-linked list of running threads.
static struct thread schedule[BBOS_NUMBER_OF_THREADS];

/**
 * bbos_thread_default_attr - Set the default attributes for scheduling.
 * @attr: Pointer to the attributes.
 */
void
bbos_thread_default_attr(void *attr)
{
}

/**
 * bbos_thread_resume - Put the thread into the list of ready threads.
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
bbos_thread_resume(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  if(schedule[tid].next != BBOS_IDLE_ID) {
    /* Sorry, but that thread is ready! */
    return BBOS_FAILURE;
  }

  if (schedule[BBOS_IDLE_ID].next == BBOS_IDLE_ID) {
    schedule[BBOS_IDLE_ID].next = tid;
  }
  else {
    schedule[schedule[BBOS_IDLE_ID].prev].next = tid;
  }

  schedule[tid].next = schedule[BBOS_IDLE_ID].next;
  schedule[tid].prev = schedule[BBOS_IDLE_ID].prev;
  schedule[BBOS_IDLE_ID].prev = tid;

  return BBOS_SUCCESS;
}

/**
 * bbos_thread_init - Initialize thread.
 * @id: Thread identifier.
 * @action: Pointer to the function.
 * @attr: Pointer to the attributes.
 */
void
bbos_thread_init(bbos_thread_id_t tid, void (*action)(), void *attr)
{
	schedule[tid].action = action;
	bbos_thread_resume(tid);
}

/**
 * bbos_thread_suspend - Remove thread from list of ready threads.
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

  /* Thread is stopped already */
  if(schedule[tid].next == BBOS_IDLE_ID) {
    return BBOS_FAILURE;
  }

  /* In the case when the scheduler consits of only one tread */
  if(((schedule[BBOS_IDLE_ID].next - tid) | (tid - schedule[BBOS_IDLE_ID].prev)) == 0) {
    schedule[BBOS_IDLE_ID].next = BBOS_IDLE_ID;
    schedule[BBOS_IDLE_ID].prev = BBOS_IDLE_ID;
  }
  else if(schedule[BBOS_IDLE_ID].next == tid) {
    schedule[BBOS_IDLE_ID].next = schedule[tid].next;
    schedule[schedule[BBOS_IDLE_ID].next].prev = schedule[BBOS_IDLE_ID].prev;
  }
  else if (schedule[BBOS_IDLE_ID].prev == tid) {
    schedule[BBOS_IDLE_ID].prev = schedule[tid].prev;
    schedule[schedule[BBOS_IDLE_ID].prev].next = schedule[BBOS_IDLE_ID].next;
  }
  else {
    schedule[schedule[tid].prev].next = schedule[tid].next;
    schedule[schedule[tid].next].prev = schedule[tid].prev;
  }

  schedule[tid].next = BBOS_IDLE_ID;
  schedule[tid].prev = BBOS_IDLE_ID;

  if(((schedule[BBOS_IDLE_ID].next - BBOS_IDLE_ID) | (schedule[BBOS_IDLE_ID].prev - BBOS_IDLE_ID)) == 0) {
    schedule[BBOS_IDLE_ID].next = BBOS_IDLE_ID;
  }

  return BBOS_SUCCESS;
}

/**
 * bbos_sched_init - Initializes the BBOS scheduler.
 */
void
bbos_sched_init()
{
	bbos_thread_id_t tid;

	target_tid = BBOS_IDLE_ID;

	for (tid=0; tid<BBOS_NUMBER_OF_THREADS; tid++) {
		schedule[tid].action = NULL;
		schedule[tid].next = BBOS_IDLE_ID;
		schedule[tid].prev = BBOS_IDLE_ID;
	}
}

void
bbos_sched_do_loop()
{
  while (1) {
    (*schedule[target_tid].action)();
    target_tid = schedule[target_tid].next;
  }
}


