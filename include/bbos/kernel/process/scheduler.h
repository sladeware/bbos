/*
 * Scheduler.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_SCHEDULER_H
#define __BBOS_SCHEDULER_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef BBOS_SCHEDULER_POLICY
#define BBOS_SCHEDULER_POLICY BBOS_SCHEDULER_FCFS_POLICY
#endif

#if BBOS_SCHEDULER_POLICY == BBOS_SCHEDULER_STATIC_POLICY
#include <bbos/kernel/process/scheduler/static.h>
#endif
#if BBOS_SCHEDULER_POLICY == BBOS_SCHEDULER_FCFS_POLICY
#include <bbos/kernel/process/scheduler/fcfs.h>
#endif

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_SCHEDULER_H */

