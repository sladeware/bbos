/*
 * Timing control.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_TIME_H
#define __BBOS_TIME_H

#define MSEC_PER_SEC (1000L)
#define USEC_PER_SEC (1000000L)

void bbos_delay_sec(uint32_t delay);
void bbos_delay_msec(uint32_t delay);
void bbos_delay_usec(uint32_t delay);

#endif /* __BBOS_TIME_H */



