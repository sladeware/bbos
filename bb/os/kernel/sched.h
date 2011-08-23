/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_SCHED_H
#define __BBOS_SCHED_H

/**
 * @file bb/os/kernel/sched.h
 * @brief Scheduler interface for thread scheduling control
 * @ingroup bbos_kernel
 */

#ifdef BBOS_SCHED_ENABLED

/**
 * Initialize scheduler.
 */
PROTOTYPE(void bbos_sched_init, ());
PROTOTYPE(void bbos_sched_move, ());
PROTOTYPE(bbos_thread_id_t bbos_sched_myself, ());

/**
 * Enqueue thread, so it will be scheduled.
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
PROTOTYPE(bbos_error_t bbos_sched_enqueue_thread, (bbos_thread_id_t tid));

/**
 * Dequeue thread, so it won't be scheduled.
 *
 * @param tid Thread identifier.
 *
 * @return
 *
 * Kernel error code.
 */
PROTOTYPE(bbos_error_t bbos_sched_dequeue_thread, (bbos_thread_id_t tid));

#endif /* BBOS_SCHED_ENABLED */

#endif /* __BBOS_SCHED_H */
