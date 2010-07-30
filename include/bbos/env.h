/*
 * The BBOS environment an attempt to build a single universal include file for
 * the whole system configurations. Generelly it containes some often-used
 * functions, prototypes, etc.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_ENV_H
#define __BBOS_ENV_H

#include <bbos/version.h>

/* Created config file. */
#include <bbos_config.h>

/* Provide hardware support. */
#include <bbos/hardware.h>

/* Some of the include files rely on architecture specific configuration. */
//#include BBOS_HARDWARE_ARCH_INC(arch_config.h)

/* General header files. */
#include <bbos/types.h>
#include <bbos/compiler.h>
#include <bbos/codes.h>
#include <bbos/debug.h>

#endif /* __BBOS_ENV_H */

