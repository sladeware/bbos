/*
 * Copyright (c) 2012 Sladeware LLC
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
#ifndef __PROPELLER_P8X32_SIO_H
#define __PROPELLER_P8X32_SIO_H

#include <bb/config.h> /* BB platform configuration */

/**
 * Receiving pin. By default is 31.
 */
#ifndef SIO_RX_PIN
#  define SIO_RX_PIN   31
#endif
/**
 * Transmitting pin. By default is 30.
 */
#ifndef SIO_TX_PIN
#  define SIO_TX_PIN   30
#endif
/**
 * Serial baudrate. By default is 115200.
 */
#ifndef SIO_BAUDRATE
#  define SIO_BAUDRATE 115200
#endif

/**
 * Defines mode bits
 *   mode bit 0 = invert rx
 *   mode bit 1 = invert tx
 *   mode bit 2 = open-drain/source tx
 *   mode bit 3 = ignore tx echo on rx
 */
#define SIO_MODE_INVERT_RX      1
#define SIO_MODE_INVERT_TX      2
#define SIO_MODE_OPENDRAIN_TX   4
#define SIO_MODE_IGNORE_TX_ECHO 8

void sio_init();

int8_t sio_get_char();
void sio_put_char(int8_t c);

#if defined(SIO_PRINTF_STRING_SUPPORT)
void sio_put_string(int8_t* s);
#endif

#if defined(SIO_PRINTF_HEX_SUPPORT)
void sio_put_hex(unsigned n);
#endif

void sio_printf(const int8_t* format, ...);

/* By default SIO_LOCK_PRINTING is enabled */
//#define SIO_LOCK_PRINTING
#define SIO_COGSAFE_PRINTING /* <! */

#ifdef SIO_COGSAFE_PRINTING
/*
 * Note, once SIO_COGSAFE_PRINTING was enabled, SIO_LOCK_PRINTING will
 * be also automatically enabled.
 */
#  define SIO_LOCK_PRINTING
void sio_cogsafe_printf(const int8_t* format, ...);
#endif /* SIO_COGSAFE_PRINTING */

#ifdef SIO_LOCK_PRINTING
void sio_lock_printf(int lock, const int8_t* format, ...);
#endif

#endif /* __PROPELLER_P8X32_SIO_H */
