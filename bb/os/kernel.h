/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

#include <bb/os/config.h>

/* Memory management */
#include <bb/os/kernel/mm.h>

enum {
  BBOS_SUCCESS = 0,
  BBOS_FAILURE
};

#include <assert.h>

#define bbos_assert(expr) assert(expr)

/*******************************************************************************
 * Threads Management
 ******************************************************************************/

extern bbos_thread_t bbos_threads[BBOS_NR_THREADS];

#define bbos_thread_set_port_id(tid, pid)       \
  do                                            \
    {                                           \
      bbos_select_thread(tid).port_id = pid;    \
    }                                           \
  while (0)

#define bbos_thread_set_target(tid, target)             \
  do                                                    \
    {                                                   \
      bbos_select_thread(tid).target = target;          \
    }                                                   \
  while (0)

#define bbos_thread_get_target(tid)             \
  bbos_select_thread(tid).target

PROTOTYPE(void bbos_thread_init, (bbos_thread_id_t tid,
                                  bbos_thread_target_t target,
                                  bbos_port_id_t pid));
PROTOTYPE(void bbos_thread_run, (bbos_thread_id_t tid));

/* Compare thread id with supported number of threads  */
#define bbos_validate_thread_id(tid) tid < BBOS_NR_THREADS

/* Select thread by its identifier. There is no another way to select thread. */
#define bbos_select_thread(tid) bbos_threads[tid]

/* Schedule thread with specified identifier. */
#define bbos_activate_thread(tid)               \
  do                                            \
    {                                           \
      printf("Activate thread '%d'\n", tid);    \
      sched_enqueue(tid);                       \
    }                                           \
  while (0)

/* This suspends a thread tid until it is manually resumed again via
   bbos_resume_thread(). */
#define bbos_suspend_thread(tid) sched_suspend(tid)

#define bbos_resume_thread(tid) sched_resume(tid)

/**
 * Stop the thread and dequeue it from schedule.
 */
#define bbos_deactivate_thread(tid)             \
  sched_dequeue(tid)

/*******************************************************************************
 * Messaging
 ******************************************************************************/

//#define bbos_message_is_(message)
#define bbos_message_set_sender(message, sender) message->sender = sender
#define bbos_message_get_sender(message) message->sender
#define bbos_message_set_command(message, command) message->command = command
#define bbos_message_get_command(message) message->command

/*******************************************************************************
 * Inter-Thread Communication
 ******************************************************************************/

/* ITC will be provided only if number of ports is greater than zero. */
#if BBOS_NR_PORTS > 0
#include <bb/os/kernel/itc.h>
#endif /* BBOS_NR_PORTS > 0 */

/*******************************************************************************
 * System Management
 ******************************************************************************/

/* Switch execution context. Start next thread selected by scheduler. */
#define bbos_switch_context()                                   \
  do                                                            \
    {                                                           \
      bbos_validate_thread_id(sched_identify_myself());         \
      bbos_thread_run(sched_identify_myself());                 \
    }                                                           \
  while (0)

PROTOTYPE(void bbos_panic, (const int8_t* fmt, ...));
PROTOTYPE(void bbos_init, ());
PROTOTYPE(void bbos_start, ());
PROTOTYPE(void bbos_stop, ());
PROTOTYPE(void bbos_main, ());
PROTOTYPE(void bbos, ());

#endif /* __BBOS_KERNEL_H */
