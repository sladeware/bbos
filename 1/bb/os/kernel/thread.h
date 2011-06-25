/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

/**
 * @file thread.h
 * @brief Thread control interface
 */

#ifndef __BBOS_THREAD_H
#define __BBOS_THREAD_H

#include <bb/os/kernel/types.h>

bbos_error_t bbos_thread_start(bbos_thread_id_t tid, bbos_thread_t thread);
bbos_error_t bbos_thread_stop(bbos_thread_id_t tid);

#endif

