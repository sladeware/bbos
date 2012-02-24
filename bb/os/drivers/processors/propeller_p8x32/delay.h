/*
 * Copyright (c) 2012 Sladeware LLC
 */
#ifdef __CATALINA__
#include <catalina_icc.h>

/* Wait for specified number of ticks */
#define bbos_delay_ticks(ticks) wait(ticks)
/* Wait for the specified number of milliseconds */
#define bbos_delay_msec(msec) msleep(msec)
void bbos_delay_usec(int usec);
#define bbos_delay_sec(sec) sleep(sec)

#elif defined(__GNUC__)
#include <sys/unistd.h>

void bbos_delay_msec(int msec);
void bbos_delay_usec(int usec);
/* Wait for the specified number of seconds */
#define bbos_delay_sec(sec) sleep(sec)

#else
#error Not supported compiler, please report support team
#endif
