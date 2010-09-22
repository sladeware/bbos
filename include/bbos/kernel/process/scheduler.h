/*
 * Scheduler.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_SCHEDULER_H
#define __BBOS_SCHEDULER_H

#ifdef __cplusplus
extern "C" {
#endif

#ifndef BBOS_SCHEDULER_POLICY
#define BBOS_SCHEDULER_POLICY basic
#endif

#if BBOS_SCHEDULER_POLICY == basic
#include <bbos/kernel/process/scheduler/basic.h>
#endif

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_SCHEDULER_H */

