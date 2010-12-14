/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko 
 */

#ifndef __BBOS_FCFS_SCHED_H
#define __BBOS_FCFS_SCHED_H

#include <bbos/config.h>

/* Scheduler interface */

void bbos_sched_init();
void bbos_sched_do_loop();

/* Scheduling policy interface */

void bbos_thread_init(bbos_thread_id_t tid,void (*action)(),void *attr);
bbos_return_t bbos_thread_suspend(bbos_thread_id_t tid);
bbos_return_t bbos_thread_resume(bbos_thread_id_t tid);

#endif

