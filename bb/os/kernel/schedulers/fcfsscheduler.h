/*
 * FCFS scheduler interface
 *
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __BBOS_FCFS_SCHEDULER_H
#define __BBOS_FCFS_SCHEDULER_H

/* Include generic scheduler interface */
#include <bb/os/kernel/schedulers/scheduler.h>

#define BBOS_SCHED_NAME "FCFS scheduler"

struct record
{
  bbos_thread_id_t next;
  bbos_thread_id_t prev;
};

#endif /* __BBOS_FCFS_SCHEDULER_H */
