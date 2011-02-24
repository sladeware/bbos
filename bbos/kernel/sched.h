
/**
 * @file sched.h
 * @brief Scheduler interface for thread scheduling control
 *
 * A scheduler is the heart of every RTOS, as it provides the algorithms to 
 * select the threads for execution.
 */

#ifndef __BBOS_SCHED_H
#define __BBOS_SCHED_H

#ifdef BBOS_SCHED_ENABLED

#include <bbos/kernel/types.h>

extern void bbos_sched_init();
extern void bbos_sched_move();
extern bbos_thread_id_t bbos_sched_myself();
extern bbos_error_t bbos_sched_enqueue(bbos_thread_id_t tid);
extern bbos_error_t bbos_sched_dequeue(bbos_thread_id_t tid);

#endif /* BBOS_SCHED_ENABLED */

#endif

