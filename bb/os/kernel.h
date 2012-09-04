/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
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
#ifndef __BB_OS_KERNEL_H
#define __BB_OS_KERNEL_H

#include <bb/os/config.h>
#if 0
#include <bb/os/kernel/mm.h>
#endif

#include "port.h"
#include "thread.h"

#include <assert.h>

typedef int16_t bbos_code_t;

/* Kernel error codes. */
enum {
  BBOS_SUCCESS = 0,
  BBOS_FAILURE
};

struct bbos_kernel_data {
  int16_t nr_threads;
  int16_t nr_ports;
};

/* Scheduler selection logic. */

/* Try to define scheduler's header file by special keywords. */
#ifndef BBOS_CONFIG_SCHED_H
#if defined(BBOS_CONFIG_USE_FCFS_SCHED)
#define BBOS_CONFIG_SCHED_H "bb/os/kernel/schedulers/fcfsscheduler.h"
#elif defined(BBOS_CONFIG_USE_STATIC_SCHED)
#define BBOS_CONFIG_SCHED_H "bb/os/kernel/schedulers/staticscheduler.h"
#endif
#endif /* BBOS_CONFIG_SCHED_H */
/* Static scheduling will be taken if scheduler wasn't selected. Use default
   scheduler header BBOS_DEFAULT_SCHED_H. */
#define BBOS_DEFAULT_SCHED_H "bb/os/kernel/schedulers/staticscheduler.h"
#ifndef BBOS_CONFIG_SCHED_H
#define BBOS_CONFIG_USE_STATIC_SCHED
#define BBOS_CONFIG_SCHED_H BBOS_DEFAULT_SCHED_H
#endif /* BBOS_CONFIG_SCHED_H */
#include BBOS_CONFIG_SCHED_H

#define bbos_kernel_assert(expr) assert(expr)

void bbos_kernel_main();

/* Returns thread structure by its identifier. */
#define bbos_kernel_get_thread(tid) bbos_kernel_threads[tid]

/* Initialize thread. */
PROTOTYPE(void bbos_kernel_init_thread, (bbos_thread_id_t tid,
                                         bbos_thread_runner_t runner));

/* Disable thread scheduling primitives in case of static scheduling policy. The
   kernel doesn't have contol over the threads. */
#ifndef BBOS_CONFIG_USE_STATIC_SCHED

/* Sets thread runner. The runner is a function to be invoked by the
   bbos_thread_run() function.

   NOTE: you cannot use this primitive in static scheduling since it doesn't
   make any sense. */
#define bbos_thread_set_runner(tid, runner)                  \
  do {                                                       \
    bbos_kernel_get_thread(tid).runner = runner;             \
  } while (0)

PROTOTYPE(void bbos_kernel_enable_all_threads, ());
PROTOTYPE(void bbos_kernel_disable_all_threads, ());
PROTOTYPE(void bbos_thread_run, (bbos_thread_id_t tid));

/*
 * Enables thread and makes it active. The system will use scheduler to schedule
 * thread by its identifier. Use bbos_kernel_disable_thread() in order to
 * disable thread. See also bbos_kernel_enable_all_threads() and
 * bbos_sched_enqueue().
 */
#define bbos_kernel_enable_thread(tid)               \
  do                                                 \
    {                                                \
      /* bbos_printf("Enable thread '%d'\n", tid);*/ \
      bbos_sched_enqueue(tid);                       \
    }                                                \
  while (0)

/* Stop thread's activity and dequeue it from schedule. Use
   bbos_kernel_enable_thread() in order to enable thread back. See also
   bbos_kernel_disable_all_threads() and bbos_sched_dequeue(). */
#define bbos_kernel_disable_thread(tid) bbos_sched_dequeue(tid)

/* Suspends thread until it is manually resumed again via
   bbos_kernel_resume_thread(). See also bbos_sched_suspend(). */
#define bbos_kernel_suspend_thread(tid) sched_suspend(tid)

/* Resumes suspended thread. See also bbos_sched_resume() and
   bbos_sched_suspend(). */
#define bbos_kernel_resume_thread(tid) bbos_sched_resume(tid)

#endif /* BBOS_CONFIG_USE_STATIC_SCHED */

/* Compares thread id with max supported number of threads BBOS_NR_THREADS. */
#define bbos_validate_thread_id(tid) assert(tid < BBOS_NR_THREADS)

// Specify the port identifier that will be used by the system for ITC.
#define bbos_thread_set_port_id(tid, pid)         \
  do {                                            \
    bbos_kernel_get_thread(tid).port_id = pid;    \
  } while (0)

#define bbos_thread_get_port_id(tid)            \
  bbos_kernel_get_thread(tid).port_id

/* Gets thread runner. */
#define bbos_thread_get_runner(tid)             \
  bbos_kernel_get_thread(tid).runner

// ITC will be provided only if number of ports is greater than zero.
#if BBOS_NR_PORTS > 0
#include <bb/os/kernel/itc.h>
#endif // BBOS_NR_PORTS > 0

////////////////////////////////////////////////////////////////////////////////
// System Management                                                          //
////////////////////////////////////////////////////////////////////////////////

#ifndef bbos_printf
//#define bbos_printf printf
#endif /* bbos_printf */

/* Halt the system. Display a message, then perform cleanups with exit. */
PROTOTYPE(void bbos_kernel_panic, (const int8_t* fmt, ...));

/* The first function that system calls, while will initialize the kernel. */
PROTOTYPE(void bbos_kernel_init, ());

PROTOTYPE(void bbos_kernel_start, ());

PROTOTYPE(void bbos_kernel_stop, ());

#endif /* __BB_OS_KERNEL_H */
