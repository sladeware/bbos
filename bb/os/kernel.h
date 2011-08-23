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

#ifdef BBOS_SCHED_ENABLED
#include <bb/os/kernel/sched.h>
#endif

#include <bb/os/kernel/system.h>

#endif /* __BBOS_KERNEL_H */
