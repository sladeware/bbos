/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_MICROKERNEL_PROCESS_H
#define __BBOS_MICROKERNEL_PROCESS_H

#include <bbos/env.h>
#include <bbos/microkernel/thread.h>
#include <bbos/microkernel/port.h>
#include <bbos/lib/memory/fastmempool.h>
#include <bbos/lib/queue.h>

/**
 * Number of ports.
 */
#ifndef BBOS_NUMBER_OF_PORTS
//#warning "BBOS_NUMBER_OF_PORTS was not defined"
#define BBOS_NUMBER_OF_PORTS 0
#endif

/**
 * The number of threads should be greater than 0, but
 * less than BBOS_MAX_NUMBER_OF_THREADS.
 */
#if BBOS_NUMBER_OF_THREADS == 0
#error "BBOS_NUMBER_OF_THREADS must be >0"
#endif
#if BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS
#error "BBOS_NUMBER_OF_THREADS > BBOS_MAX_NUMBER_OF_THREADS"
#endif

extern bbos_thread_t bbos_process_thread_table[BBOS_NUMBER_OF_THREADS];

extern bbos_port_t bbos_process_port_table[BBOS_NUMBER_OF_PORTS];

/* Prototypes */

void bbos_process_init();

#endif /* __BBOS_MICROKERNEL_PROCESS_H */


