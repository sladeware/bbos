// Static scheduling interface
//
// Copyright (c) 2012 Sladeware LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Author: Oleksandr Sviridenko

#ifndef __BB_OS_KERNEL_SCHEDULERS_STATIC_SCHEDULER_H
#define __BB_OS_KERNEL_SCHEDULERS_STATIC_SCHEDULER_H

// Include generic scheduler interface
#include <bb/os/kernel/schedulers/scheduler.h>
#define BBOS_SCHED_NAME "Static scheduler"

#define bbos_sched_init()
#define bbos_sched_enqueue(tid)
#define bbos_sched_dequeue(tid)

#endif // __BB_OS_KERNEL_SCHEDULERS_STATIC_SCHEDULER_H
