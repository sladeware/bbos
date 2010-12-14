/*
 * System.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_SYSTEM_H
#define __BBOS_SYSTEM_H

/* Enumerate values used for system states */
extern enum bbos_system_states {
	BBOS_SYSTEM_INITIALIZATION,
	BBOS_SYSTEM_TESTING,
	BBOS_SYSTEM_RUNNING
} bbos_system_state;

extern void bbos_panic(const char *fmt, ...);

#endif

