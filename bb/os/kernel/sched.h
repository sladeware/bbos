/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/os/kernel/sched.h
 * @brief Scheduler interface for thread scheduling control
 * @ingroup bbos_kernel
 */

#if defined(BBOS_SCHED_CONFIG_H)
#ifdef __BBOS_SCHED_H
#error "Scheduler was already selected"
#else
#define __BBOS_SCHED_H
#endif /* BBOS_SCHED_ENABLED */
#endif /* checking for BBOS_SCHED_CONFIG_H */

#ifndef __BBOS_SCHED_H
#define __BBOS_SCHED_H

/**
 * Initialize scheduler.
 */
PROTOTYPE(void bbos_sched_init, ());

/**
 * Move to the next thread in schedule.
 */
PROTOTYPE(void bbos_sched_move, ());

/**
 * This function is opposite to bbos_sched_move(). It breaks scheduling order
 * and jump to specified thread. This widely used
 * in static scheduling when we always jump from one thread to another. It
 * also has to provide opportunity for thread identification
 * bbos_sched_identify().
 * @param tid Thread identifier
 * @see bbos_sched_move()
 * @see bbos_sched_identify()
 */
PROTOTYPE(void bbos_sched_jump, (bbos_thread_id_t tid));

/**
 * Identify running thread and return its id.
 * @return Thread identifier.
 */
PROTOTYPE(bbos_thread_id_t bbos_sched_identify, ());

/**
 * Enqueue thread, so it will be scheduled.
 * @param tid Thread identifier.
 * @return Kernel error code.
 */
PROTOTYPE(bbos_error_t bbos_sched_enqueue, (bbos_thread_id_t tid));

/**
 * Dequeue thread, so it won't be scheduled.
 * @param tid Thread identifier.
 * @return Kernel error code.
 */
PROTOTYPE(bbos_error_t bbos_sched_dequeue, (bbos_thread_id_t tid));

#endif /* __BBOS_SCHED_H */
