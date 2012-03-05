/*
 * Kernel config
 *
 * Copyright (c) 2012 Sladeware LLC
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
#ifndef __BBOS_KERNEL_CONFIG_H
#define __BBOS_KERNEL_CONFIG_H

/* Check number of threads. */
#ifndef BBOS_CONFIG_NR_THREADS
# error Please define BBOS_CONFIG_NR_THREADS in BB_CONFIG_OS_H
#endif
#if BBOS_CONFIG_NR_THREADS < 1
# error System requires atleast one thread
#endif

/* System threads */
#define BBOS_NR_SYSTEM_THREADS 1
#define BBOS_IDLE BBOS_CONFIG_NR_THREADS + 0

/* Set final number of threads */
#define BBOS_NR_THREADS (BBOS_CONFIG_NR_THREADS + BBOS_NR_SYSTEM_THREADS)

/* By default the number of ports in zero. In this case port interface wont be
   supported. */
#ifndef BBOS_CONFIG_NR_PORTS
# define BBOS_CONFIG_NR_PORTS 0
#endif
#define BBOS_NR_PORTS BBOS_CONFIG_NR_PORTS

/* Scheduler selection logic. If scheduler wasn't selected, FCFS scheduler
   will be taken. */
#ifndef BBOS_COFNIG_SCHED_H
# include <bb/os/kernel/config/scheduler.h>
#endif
#include BBOS_CONFIG_SCHED_H

#endif /* __BBOS_KERNEL_CONFIG_H */
