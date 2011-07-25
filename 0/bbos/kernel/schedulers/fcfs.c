
#include <bbos/config.h>
#include <bbos/kernel/types.h>
#include <bbos/kernel/error_codes.h>
#include <bbos/kernel/debug.h>

static bbos_thread_id_t myself = BBOS_IDLE;

bbos_thread_id_t
bbos_sched_myself()
{
  return myself;
}

struct record {
  bbos_thread_id_t next;
  bbos_thread_id_t prev;
};

static struct record schedule[BBOS_NUMBER_OF_THREADS];

bbos_error_t
bbos_sched_enqueue(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);
  
  if(schedule[tid].next != BBOS_IDLE)
    return BBOS_FAILURE;

  if (schedule[BBOS_IDLE].next == BBOS_IDLE)
    schedule[BBOS_IDLE].next = tid;
  else
    schedule[schedule[BBOS_IDLE].prev].next = tid;

  schedule[tid].next = schedule[BBOS_IDLE].next;
  schedule[tid].prev = schedule[BBOS_IDLE].prev;
  schedule[BBOS_IDLE].prev = tid;

  return BBOS_SUCCESS;
}

bbos_error_t
bbos_sched_dequeue(bbos_thread_id_t tid)
{
  assert(tid <= BBOS_NUMBER_OF_THREADS);

  if(schedule[tid].next == BBOS_IDLE)
    return BBOS_FAILURE;

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

  if(((schedule[BBOS_IDLE].next - BBOS_IDLE) | (schedule[BBOS_IDLE].prev - BBOS_IDLE)) == 0)
    schedule[BBOS_IDLE].next = BBOS_IDLE;

  return BBOS_SUCCESS;
}

void
bbos_sched_init()
{
  bbos_thread_id_t tid;

  for (tid=0; tid<BBOS_NUMBER_OF_THREADS; tid++)
    {
      schedule[tid].next = BBOS_IDLE;
      schedule[tid].prev = BBOS_IDLE;
    }
}

void
bbos_sched_move()
{
  myself = schedule[ bbos_sched_myself() ].next;
}

