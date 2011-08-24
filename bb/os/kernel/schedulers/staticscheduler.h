/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/os/kernel/schedulers/staticscheduler.h
 * @brief Static scheduler
 */
#ifndef __BBOS_STATICSCHED_H
#define __BBOS_STATICSCHED_H

#include <bb/os/kernel/sched.h>

#define BBOS_SCHED_STR "Static scheduler"

EXTERN bbos_thread_id_t bbos_x;

#define bbos_sched_init()                       \
  0

#define bbos_sched_move()                       \
  0

#define bbos_sched_jump(tid)                    \
  do{                                           \
    bbos_x = tid;                               \
  } while (0)

#define bbos_sched_identify() bbos_x

#define bbos_sched_enqueue(tid)                 \
  do { } while (0)

#define bbos_sched_dequeue(tid)                 \
  do { } while (0)

#endif /* __BBOS_STATICSCHED_H */
