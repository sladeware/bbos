/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_PROCESS_H
#define __BBOS_PROCESS_H

#ifdef __cplusplus
extern "C" {
#endif

/* Threads */
#include <bbos/kernel/process/thread.h>

/* Scheduler */
#include <bbos/kernel/process/scheduler.h>

/* Inter-thread communication support */
#include <bbos/kernel/process/itc.h>

/* Prototypes */

void bbos_process_init();

void bbos_process_test();

void bbos_process_start();

void bbos_process_stop();

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_PROCESS_H */


