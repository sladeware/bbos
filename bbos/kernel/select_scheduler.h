/*
 * Select scheduler.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifdef BBOS_DISABLE_SCHEDULER

#elif !defined(BBOS_SCHEDULER_FILE)

#ifdef BBOS_FCFS_SCHEDULER
#	define BBOS_SCHEDULER_FILE <bbos/kernel/schedulers/fcfs.h>
#endif

#endif

#ifdef BBOS_SCHEDULER_FILE
#	include BBOS_SCHEDULER_FILE
#endif

