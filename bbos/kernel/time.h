/*
 * Time management.
 * 
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_TIME_H
#define __BBOS_TIME_H

#define MSEC_PER_SEC (1000L)
#define USEC_PER_SEC (1000000L)
#define NSEC_PER_SEC (1000000000L)

#ifdef __CATALINA__
#define bbos_delay_sec(delay) _waitcnt(_cnt() + delay * 100000000L)
#define bbos_delay_msec(delay) _waitcnt(_cnt() + delay * 100000L)
#define bbos_delay_usec(delay) _waitcnt(_cnt() + delay * 10L)
#endif

#endif


