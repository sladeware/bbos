/*
 * Copyright (c) 2012-2013 Sladeware LLC
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
 *
 * Author: Oleksandr Sviridenko
 */
#ifndef __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SIO_H
#define __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SIO_H

#include <bb/config.h>
#include BB_STDLIB_FILE(stdarg.h)

/* Default definitions */
#define BB_PRINTF_STRING_SUPPORT

/* Receiving pin. */
#ifndef SIO_RX_PIN
#define SIO_RX_PIN 31
#endif
/* Transmitting pin. */
#ifndef SIO_TX_PIN
#define SIO_TX_PIN 30
#endif
/* Serial baudrate. */
#ifndef SIO_BAUDRATE
#define SIO_BAUDRATE 115200
#endif

#define SIO_MODE_INVERT_RX      1
#define SIO_MODE_INVERT_TX      2
#define SIO_MODE_OPENDRAIN_TX   4
#define SIO_MODE_IGNORE_TX_ECHO 8

/* Prototypes. */

/* Receives a character to serial. Return 8-bit character. */
char bb_get_byte();

char bb_wait_byte_with_timeout(int16_t secs);

char bb_wait_byte();

/* Writes a character to the serial. This function is safe to changing of clock
   frequency. */
void bb_put_byte(char c);

#if defined(BB_PRINTF_STRING_SUPPORT)
void bb_put_string(char* s);
#endif

#if defined(BB_PRINTF_HEX_SUPPORT)
void bb_put_hex(unsigned n);
#endif

/* See http://en.wikipedia.org/wiki/Printf#Format_placeholders */
void bb_printf(const char* format, ...);
void bb_vprintf(const char* format, va_list a);

#ifdef SIO_COGSAFE_PRINTING
/* NOTE: once SIO_COGSAFE_PRINTING was enabled, SIO_LOCK_PRINTING will be also
   automatically enabled. */
#define SIO_LOCK_PRINTING
void sio_cogsafe_printf(const char* format, ...);
#endif /* SIO_COGSAFE_PRINTING */

#ifdef SIO_LOCK_PRINTING
/* Lock printing routine. This routine assumes that propeller_locknew() was used
   before. */
void sio_lock_printf(int lock, const char* format, ...);
#endif

#endif /* __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_SIO_H */
