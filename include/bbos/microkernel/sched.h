/*
 * The scheduler.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_SCHED_H
#define __BBOS_MICROKERNEL_SCHED_H

#include <bbos/env.h>

extern bbos_thread_id_t bbos_sched_pending;

extern bbos_thread_id_t bbos_sched_myself;

/**
 * bbos_sched_jump - Jumps to the target thread.
 * @tid: Thread identifier on which we jump.
 *
 * Jumps to the target thread after the current thread is finished. After
 * the jump, the scheduler will execute the new thread.
 */
#define bbos_sched_jump(tid)\
  bbos_sched_pending = tid

/* Prototypes */

void bbos_sched_init();

bbos_return_t bbos_sched_next();

#endif /* __BBOS_MICROKERNEL_SCHED_H */

