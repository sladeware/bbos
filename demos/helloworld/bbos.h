/*
 * Tue Mar  8 22:36:35 2011
 *
 * This is BBOS generated source code used for late binding application
 * features just before compile time.
 *
 * Please do not edit this by hand, as your changes will be lost.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
#ifndef __BBOS_H
#define __BBOS_H
/* Threads */
#define BBOS_NUMBER_OF_THREADS (2)
#define BBOS_IDLE (0)
#define HELLOWORLD (1)
/* Messages */
#define BBOS_NUMBER_OF_MESSAGES (3)
#define BBOS_DRIVER_INIT (0)
#define BBOS_DRIVER_CLOSE (1)
#define BBOS_DRIVER_OPEN (2)
/* Scheduling */
#define bbos_switch_thread()\
	while(1) {\
		helloworld();\
	}
#endif /* __BBOS_H */
