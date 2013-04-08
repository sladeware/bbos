/*
 * Common scheduler interface for thread scheduling control
 *
 * Copyright (c) 2012-2013 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifdef BBOS_CONFIG_SCHED_H
# ifdef __BBOS_SCHED_H
#  error Scheduler was already included
# endif /* checking for BBOS_CONFIG_SCHED_H */
#endif

#ifndef __BB_OS_KERNEL_SCHEDULERS_SCHEDULER_H
#define __BB_OS_KERNEL_SCHEDULERS_SCHEDULER_H

/**
 * Initializes scheduler.
 */
PROTOTYPE(void bbos_sched_init, ());

/* Move to the next thread in schedule. */
PROTOTYPE(void bbos_sched_move, ());

/* Return thread identifier that has to be executed on this moment. */
PROTOTYPE(bbos_thread_id_t bbos_sched_identify_myself, ());

/**
 * This function is opposite to bbos_sched_move(). It breaks scheduling order
 * and jumps to specified thread. This is widely used on static scheduling when
 * we always jump from one thread to another. Developer should be careful and
 * provide opportunity for thread identification.
 */
PROTOTYPE(void bbos_sched_jump, (bbos_thread_id_t id));

/**
 * Enqueues thread so it will be scheduled.
 */
PROTOTYPE(void bbos_sched_enqueue, (bbos_thread_id_t id));

/**
 * Dequeues thread so it won't be scheduled.
 */
PROTOTYPE(void bbos_sched_dequeue, (bbos_thread_id_t tid));

/**
 * This suspends a thread until it is manually resumed again via
 * bbos_sched_resume().
 */
PROTOTYPE(void bbos_sched_suspend, (bbos_thread_id_t tid));

PROTOTYPE(void bbos_sched_resume, (bbos_thread_id_t tid));

#endif /* __BB_OS_KERNEL_SCHEDULERS_SCHEDULER_H */
