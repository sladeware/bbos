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

/* Scheduler selection logic. */
#ifndef BBOS_SCHED_CONFIG_H
#define BBOS_SCHED_CONFIG_H "bb/os/kernel/schedulers/staticscheduler.h"
#endif
#include BBOS_SCHED_CONFIG_H

#include <bb/os/kernel/system.h>

#endif /* __BBOS_KERNEL_H */
