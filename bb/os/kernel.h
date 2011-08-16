/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_KERNEL_H
#define __BBOS_KERNEL_H

#include <bb/os/config.h> /* MUST be first */
#include <bb/os/kernel/errors.h>
#include <bb/os/kernel/types.h>

#include <limits.h>

#ifdef BBOS_SCHED_ENABLED
#include <bb/os/kernel/sched.h>
#endif

#include <bb/os/kernel/system.h>

#endif /* __BBOS_KERNEL_H */
