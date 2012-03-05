/*
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

#include <bb/os/config.h>
#include <bb/os/kernel/mm.h> /* Memory management */
#include <bb/os/kernel/error_codes.h>

#include <assert.h>

#define bbos_kernel_assert(expr) assert(expr)

/* List of kernel threads. */
extern bbos_thread_t bbos_kernel_threads[BBOS_NR_THREADS];

#define bbos_message_set_owner(message, owner) \
  do {\
    message->owner = owner;\
  } while(0)

#define bbos_message_set_command(message, command) \
  do {\
    message->command = command;\
  } while(0)

#define bbos_message_get_owner(message) \
  message->owner

#define bbos_message_get_command(message) \
  message->command

/*******************************************************************************
 * The following kernel functionality aims to control and manage
 * threads.
 ******************************************************************************/

/**
 * Get thread by its identifier. Please use this primitive insead of
 * direct access bbos_kernel__threads array.
 */
#define bbos_kernel_get_thread(tid) bbos_kernel_threads[tid]

PROTOTYPE(void bbos_kernel_init_thread, (bbos_thread_id_t tid,
                                         bbos_thread_runner_t runner,
                                         bbos_port_id_t pid));
PROTOTYPE(void bbos_kernel_enable_all_threads, ());
PROTOTYPE(void bbos_kernel_disable_all_threads, ());
PROTOTYPE(void bbos_thread_run, (bbos_thread_id_t tid));

/**
 * Enable thread and make it active. The system will use scheduler to
 * schedule thread by its identifier. Use bbos_kernel_disable_thread()
 * in order to disable thread. See also
 * bbos_kernel_enable_all_threads() and bbos_sched_enqueue().
 */
#define bbos_kernel_enable_thread(tid)               \
  do                                                 \
    {                                                \
      /* bbos_printf("Enable thread '%d'\n", tid);*/ \
      bbos_sched_enqueue(tid);                       \
    }                                                \
  while (0)

/**
 * Stop thread's activity and dequeue it from schedule. Use
 * bbos_kernel_enable_thread() in order to enable thread back.
 * See also bbos_kernel_disable_all_threads() and
 * bbos_sched_dequeue().
 */
#define bbos_kernel_disable_thread(tid) bbos_sched_dequeue(tid)

/**
 * Suspend thread until it is manually resumed again via
 * bbos_kernel_resume_thread(). See also bbos_sched_suspend().
 */
#define bbos_kernel_suspend_thread(tid) sched_suspend(tid)

/**
 * Resume suspended thread. See also bbos_sched_resume() and
 * bbos_sched_suspend().
 */
#define bbos_kernel_resume_thread(tid) bbos_sched_resume(tid)

/*******************************************************************************
 * The folloing interface provides thread control primitives.
 ******************************************************************************/

/**
 * Compare thread id with max supported number of threads
 * BBOS_NR_THREADS.
 */
#define bbos_validate_thread_id(tid) assert(tid < BBOS_NR_THREADS)

/**
 * Specify the port identifier that will be used by the system for
 * ITC.
 */
#define bbos_thread_set_port_id(tid, pid)         \
  do                                              \
    {                                             \
      bbos_kernel_get_thread(tid).port_id = pid;  \
    }                                             \
  while (0)

#define bbos_thread_get_port_id(tid)            \
  bbos_kernel_get_thread(tid).port_id

/**
 * Set thread runner. The runner is a function to be invoked by the
 * bbos_thread_run() function.
 */
#define bbos_thread_set_runner(tid, runner)                 \
  do                                                        \
    {                                                       \
      bbos_kernel_get_thread(tid).runner = runner;          \
    }                                                       \
  while (0)

/**
 * Get thread runner.
 */
#define bbos_thread_get_runner(tid)             \
  bbos_kernel_get_thread(tid).runner

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

/**
 * Switch execution context. Start next thread selected by scheduler.
 */
#define bbos_kernel_switch_context()                                 \
  do                                                                 \
    {                                                                \
      bbos_validate_thread_id(bbos_sched_identify_myself());         \
      bbos_thread_run(bbos_sched_identify_myself());                 \
    }                                                                \
  while (0)

#ifdef BBOS_CONFIG_KERNEL_LOOP
void bbos_kernel_loop();
#endif

PROTOTYPE(void bbos_kernel_panic, (const int8_t* fmt, ...));
PROTOTYPE(void bbos_kernel_init, ());
PROTOTYPE(void bbos_kernel_start, ());
PROTOTYPE(void bbos_kernel_stop, ());

#endif /* __BBOS_KERNEL_H */
