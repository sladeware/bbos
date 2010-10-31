/*
 * Process.
 *
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_PROCESS_H
#define __BBOS_PROCESS_H

#ifdef __cplusplus
extern "C" {
#endif

#include <bbos/kernel/process/thread.h>
#include <bbos/kernel/process/scheduler.h>
#include <bbos/kernel/process/port.h>

/* Include system threads */
#include <bbos/kernel/process/thread/idle.h>
#include <bbos/kernel/process/thread/main.h>

/* Prototypes */

void bbos_process_init();
void bbos_process_start();
void bbos_process_stop();

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_PROCESS_H */


