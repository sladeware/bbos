/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <stdio.h>

#include <bb/os/config.h>
#include <bb/os/kernel/thread.h>
#include <bb/os/kernel/sched.h>
#include <bb/os/kernel/errors.h>
#include <bb/os/kernel/debug.h>

static bbos_thread_t bbos_thread_table[BBOS_NUMBER_OF_THREADS];

void
bbos_thread_init(bbos_thread_id_t tid, void (*thread)(void))
{
  bbos_thread_table[tid] = thread;
}

void
bbos_thread_run(bbos_thread_id_t tid)
{
  assert(bbos_thread_table[tid] != NULL);
  (*bbos_thread_table[tid])();
}

