/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

/**
 * @defgroup bbos_kernel Kernel
 **/
/**
 * @file kernel.h
 * @brief Master header file for the kernel.
 * @ingroup bbos_kernel
 */

#include <bb/os/config.h> /* MUST be first */
#include <bb/os/kernel/errors.h>

#ifndef BBOS_CONFIG_NR_THREADS
# error Please define BBOS_CONFIG_NR_THREADS in BB_CONFIG_OS_H
#endif
#define BBOS_NR_THREADS BBOS_CONFIG_NR_THREADS

/* Scheduler selection logic */
#ifndef BBOS_CONFIG_SCHED_H
# define BBOS_CONFIG_SCHED_H "bb/os/kernel/schedulers/staticscheduler.h"
#endif
#include BBOS_CONFIG_SCHED_H

#include <bb/os/kernel/system.h>

#endif /* __BBOS_KERNEL_H */
