/*
 * The BBOS main header file.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_H
#define __BBOS_H

/**
 * Allows application to know that BBOS are in use.
 */
#define BBOS

/* Microkernel header files */
#include <bbos/microkernel/sys.h>
#include <bbos/microkernel/port.h>
#include <bbos/microkernel/process.h>
#include <bbos/microkernel/sched.h>
#include <bbos/microkernel/itc.h>

#endif /* __BBOS_H */

