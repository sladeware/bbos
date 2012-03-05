/*
 * Scheduler selection logic
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

#define BBOS_DEFAULT_SCHED_H "bb/os/kernel/schedulers/fcfsscheduler.h"

/* Try to define scheduler's header file by special keywords. */
#ifndef BBOS_CONFIG_SCHED_H
#  if defined(BBOS_CONFIG_USE_FCFS_SCHED)
#    define BBOS_CONFIG_SCHED_H "bb/os/kernel/schedulers/fcfsscheduler.h"
#  elif defined(BBOS_CONFIG_USE_STATIC_SCHED)
#    define BBOS_CONFIG_SCHED_H "bb/os/kernel/schedulers/staticscheduler.h"
#  endif
#endif /* BBOS_CONFIG_SCHED_H */

/* Select default scheduler header BBOS_DEFAULT_SCHED_H. */
#ifndef BBOS_CONFIG_SCHED_H
#  define BBOS_CONFIG_SCHED_H BBOS_DEFAULT_SCHED_H
#endif /* BBOS_CONFIG_SCHED_H */
