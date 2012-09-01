/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_DELAY_H
#define __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_DELAY_H

#include <bb/os/drivers/processors/propeller_p8x32/config.h>

/*
 * The minimal waitcnt() windows value must always be at least 381 to
 * avoid unexpectedly long delays.
 */
#define MIN_WAITCNT_WINDOW 381

static int int_max(int a, int b)
{
  b = a - b;
  a -= b & (b >> 31);
  return a;
}

/* Millisecond delay. */
#define BBOS_DELAY_MSEC(msec)                                           \
  propeller_waitcnt(int_max((propeller_get_clockfreq() / 1000) * msec - 3932, \
                            MIN_WAITCNT_WINDOW) +                       \
                    propeller_get_cnt())

/* Catalina compiler specific interface. */
#if defined(__CATALINA__)
#include <catalina_icc.h>
/* Wait for specified number of ticks. */
#define bbos_delay_ticks(ticks) wait(ticks)
/* Wait for the specified number of milliseconds. */
#define bbos_delay_msec(msec) msleep(msec)
void bbos_delay_usec(int usec);
#define bbos_delay_sec(sec) sleep(sec)

/* GNUC compiler specific interface. */
#elif defined(__GNUC__)
#include <sys/unistd.h>

void bbos_delay_msec(int msec);
void bbos_delay_usec(int usec);
/* Wait for the specified number of seconds. */
#define bbos_delay_sec(sec) sleep(sec)

#else
#error Not supported compiler, please report support team
#endif /* __CATALINA__ */

#endif /* __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_DELAY_H */
