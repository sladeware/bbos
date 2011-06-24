/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <stdio.h>

#include <bbos/config.h>
#include <bbos/kernel/thread.h>
#include <bbos/kernel/sched.h>
#include <bbos/kernel/error_codes.h>
#include <bbos/kernel/debug.h>

static bbos_thread_t bbos_thread_table[BBOS_NUMBER_OF_THREADS];

void
bbos_thread_init(bbos_thread_id_t tid, void (*thread)(void))
{
  bbos_thread_table[tid] = thread;
}

void
bbos_thread_execute(bbos_thread_id_t tid)
{
	assert(bbos_thread_table[tid] != NULL);
	(*bbos_thread_table[tid])();
}

