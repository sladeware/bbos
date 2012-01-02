/*
 * FCFS scheduler
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/os.h>

static bbos_thread_id_t cursor = BBOS_IDLE;
static struct record schedule[BBOS_NR_THREADS];

void
sched_init()
{
  for (cursor=0; cursor<BBOS_NR_THREADS; cursor++)
    {
      schedule[cursor].next = BBOS_IDLE;
      schedule[cursor].prev = BBOS_IDLE;
    }
  cursor = BBOS_IDLE;
}

bbos_thread_id_t
sched_identify_myself()
{
  return cursor;
}

void
sched_move()
{
  cursor = schedule[cursor].next;
}

bbos_code_t
sched_enqueue(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  if(schedule[tid].next != BBOS_IDLE)
    {
      printf("111 %d\n", tid);
      return BBOS_FAILURE;
    }
  if (schedule[BBOS_IDLE].next == BBOS_IDLE)
    {
      schedule[BBOS_IDLE].next = tid;
    }
  else
    {
      schedule[schedule[BBOS_IDLE].prev].next = tid;
    }
  schedule[tid].next = schedule[BBOS_IDLE].next;
  schedule[tid].prev = schedule[BBOS_IDLE].prev;
  schedule[BBOS_IDLE].prev = tid;
  return BBOS_SUCCESS;
}

bbos_code_t
sched_dequeue(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  if(schedule[tid].next == BBOS_IDLE)
    {
      /* Thread can not be dequeued. You are trying to dequeue thread that was
       not scheduled or the schedule was broken. */
      return BBOS_FAILURE;
    }
  if(((schedule[BBOS_IDLE].next - tid) | (tid - schedule[BBOS_IDLE].prev)) == 0)
    {
      schedule[BBOS_IDLE].next = BBOS_IDLE;
      schedule[BBOS_IDLE].prev = BBOS_IDLE;
    }
  else if(schedule[BBOS_IDLE].next == tid)
    {
      schedule[BBOS_IDLE].next = schedule[tid].next;
      schedule[schedule[BBOS_IDLE].next].prev = schedule[BBOS_IDLE].prev;
    }
  else if (schedule[BBOS_IDLE].prev == tid)
    {
      schedule[BBOS_IDLE].prev = schedule[tid].prev;
      schedule[schedule[BBOS_IDLE].prev].next = schedule[BBOS_IDLE].next;
    }
  else
    {
      schedule[schedule[tid].prev].next = schedule[tid].next;
      schedule[schedule[tid].next].prev = schedule[tid].prev;
    }
  schedule[tid].next = BBOS_IDLE;
  schedule[tid].prev = BBOS_IDLE;
  if(((schedule[BBOS_IDLE].next - BBOS_IDLE)
      | (schedule[BBOS_IDLE].prev - BBOS_IDLE)) == 0)
    {
      schedule[BBOS_IDLE].next = BBOS_IDLE;
    }
  return BBOS_SUCCESS;
}
