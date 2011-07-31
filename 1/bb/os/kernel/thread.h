/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file thread.h
 * @brief Thread control interface
 */

#ifndef __BBOS_THREAD_H
#define __BBOS_THREAD_H

#include <bb/os/kernel/types.h>

void bbos_thread_init(bbos_thread_id_t tid, bbos_thread_t thread);
void bbos_thread_run(bbos_thread_id_t tid);

#endif

