/*
 * Common scheduler interface for thread scheduling control
 *
 * Copyright (c) 2011 Sladeware LLC
 */
#ifdef BBOS_CONFIG_SCHED_H
# ifdef __BBOS_SCHED_H
#  error Scheduler was already included
# endif /* checking for BBOS_CONFIG_SCHED_H */
#endif

#ifndef __BBOS_SCHED_H
#define __BBOS_SCHED_H

/* Initialize scheduler. */
PROTOTYPE(void sched_init, ());

/* Move to the next thread in schedule. */
PROTOTYPE(void sched_move, ());

/* Return thread identifier that has to be executed on this moment. */
PROTOTYPE(bbos_thread_id_t sched_identify_myself, ());

/* This function is opposite to sched_move(). It breaks scheduling order
   and jumps to specified thread. This is widely used on static scheduling when
   we always jump from one thread to another. Developer should be careful and
   provide opportunity for thread identification. */
PROTOTYPE(void sched_jump, (bbos_thread_id_t tid));

/* Enqueue thread so it will be scheduled. */
PROTOTYPE(bbos_code_t sched_enqueue, (bbos_thread_id_t tid));

/* Dequeue thread so it won't be scheduled. */
PROTOTYPE(bbos_code_t sched_dequeue, (bbos_thread_id_t tid));

/* This suspends a thread until it is manually resumed again via
   sched_resume(). */
PROTOTYPE(bbos_code_t sched_suspend, (bbos_thread_id_t tid));

PROTOTYPE(bbos_code_t sched_resume, (bbos_thread_id_t tid));

#endif /* __BBOS_SCHED_H */
