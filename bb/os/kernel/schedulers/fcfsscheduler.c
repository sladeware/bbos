/*
 * FCFS scheduler.
 *
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <bb/os.h>

static bbos_thread_id_t cursor = BBOS_IDLE;
static struct record schedule[BBOS_NR_THREADS];

void
bbos_sched_init()
{
  for (cursor = 0; cursor < BBOS_NR_THREADS; cursor++)
    {
      schedule[cursor].next = BBOS_IDLE;
      schedule[cursor].prev = BBOS_IDLE;
    }
  cursor = BBOS_IDLE;
}

bbos_thread_id_t
bbos_sched_identify_myself()
{
  return cursor;
}

void
bbos_sched_move()
{
  cursor = schedule[cursor].next;
}

bbos_code_t
bbos_sched_enqueue(bbos_thread_id_t tid)
{
  bbos_validate_thread_id(tid);
  if(schedule[tid].next != BBOS_IDLE)
    {
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
bbos_sched_dequeue(bbos_thread_id_t tid)
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
