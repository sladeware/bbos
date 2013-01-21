/*
 * This files implements sio.h interface.
 *
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
 *
 * Note, sio_put_byte() and sio_get_byte() is the only external dependency for
 * this file.
 */

/*
 * TODO: revise lock-safe routines.
 */
#include "sio.h"
#include "pins.h"
#include "delay.h"

#define SIO_CNT_DELTA 500

HUBTEXT char
bb_wait_byte()
{
  while (GET_INPUT(SIO_RX_PIN));
  return bb_get_byte();
}

HUBTEXT char
bb_wait_byte_with_timeout(int16_t secs)
{
  char byte;
  int32_t counts_delta = 0;
  int32_t start_counts;

  counts_delta = secs * propeller_get_clockfreq();
  start_counts = propeller_get_cnt();
  while ((propeller_get_cnt() - start_counts) < counts_delta) {
    if ((byte = bb_get_byte())) {
      return byte;
    }
  }
  return 0;
}

HUBTEXT char
bb_get_byte()
{
  int8_t i;
  int16_t byte;
  byte = 0;
  /* Check start bit on rx pin. */
  if (GET_INPUT(SIO_RX_PIN)) {
    return byte;
  }
  /* Start reading a byte... */
  for (i = 0; i < 8; i++) {
    propeller_waitcnt(SIO_CNT_DELTA + propeller_get_cnt());
    byte = ((0 != (propeller_get_ina_bits() & GET_MASK(SIO_RX_PIN))) << 7) | (byte >> 1);
  }
  /* Fix and return byte. */
  byte >>= 1;
  return (char)byte;
}

/* NOTE: We need bb_put_byte() to always be in HUB memory for speed.
   Time critical functions like this can't live in external memory. */
HUBTEXT void
bb_put_byte(char c)
{
  int frame = 0;
  //int i = 11;
  uint32_t bitticks_cnt;
  uint32_t num_bitticks;

  num_bitticks = propeller_get_clockfreq() / SIO_BAUDRATE;
  DIR_OUTPUT(SIO_TX_PIN);

#if 1
  /* Frame format: 1 _ _ _ _ _ _ _ _ 0 1 */
  frame = 0x400 | (c << 2) | 1;

  OUT_HIGH(SIO_TX_PIN);
  frame >>= 1;

  /* Start to transmit frame's bits one by one  */
  bitticks_cnt = propeller_get_cnt() + num_bitticks;
#define TR_BIT \
  do {\
  bitticks_cnt = __builtin_propeller_waitcnt(bitticks_cnt, num_bitticks); \
  OUT_TO(SIO_TX_PIN, (frame & 1));              \
  frame >>= 1;\
  } while (0)

  //TR_BIT;
  TR_BIT;

  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;
  TR_BIT;

  TR_BIT;

  BBOS_DELAY_MSEC(1);

  DIR_INPUT(SIO_TX_PIN);
  OUT_LOW(SIO_TX_PIN);
#endif
#if 0
  /* Frame format: 1 _ _ _ _ _ _ _ _ 0 1 */
  frame = 0x400 | (c << 2) | 1;

  /* Start to transmit frame's bits one by one  */
  bitticks_cnt = propeller_get_cnt();
  do
    {
      bitticks_cnt += num_bitticks;  /* ready next bit period */
      /* ensure that bit transmit period done */
      while (bitticks_cnt > propeller_get_cnt());
      OUT_TO(SIO_TX_PIN, (frame & 1));
      /* move to the next bit */
      frame >>= 1;
    } while (i--);
  /* We need a *very* small delay to notify about transmission
     ending. */

  //BBOS_DELAY_MSEC(1);
#endif

  /* XXX: if we turn off DIRA, then some boards (like QuickStart) are
     left with floating pins and garbage output; if we leave it on,
     we're left with a high pin and other cogs cannot produce output
     on it the solution is to use FullDuplexSerialDriver instead on
     applications with multiple cogs

     _DIRA &= ~txmask; */

  /* NOTE: the following code is unrolled version of while-loop
     statement. Note, this version is a little bit faster and
     takes more code, but in some reason doesn't support multicog
     running. */
#if 0
#define TRANSMIT_BIT                              \
  do                                              \
    {                                             \
      OUT_TO(SIO_TX_PIN, (frame & 1));            \
      frame >>= 1;                                \
      bitticks_cnt += num_bitticks;               \
      while (bitticks_cnt > propeller_get_cnt()); \
    } while (0)

  TRANSMIT_BIT;

  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;
  TRANSMIT_BIT;

  TRANSMIT_BIT;
  TRANSMIT_BIT;
#endif
}

#if defined(BB_PRINTF_STRING_SUPPORT)
void
bb_put_string(char* s)
{
  while (*s) {
    bb_put_byte(*s++);
  }
}
#endif /* BB_PRINTF_STRING_SUPPORT */

static const unsigned long dv[] = {
#if 0
  4294967296,     /* 32 bit unsigned max */
#endif
  1000000000,     /* +0 */
  100000000,     /* +1 */
  10000000,     /* +2 */
  1000000,     /* +3 */
  100000,     /* +4 */
#if 0
  65535,    /* 16 bit unsigned max */
#endif
  10000,  /* +5 */
  1000,  /* +6 */
  100,  /* +7 */
  10,  /* +8 */
  1,  /* +9 */
};

static void
xtoa(unsigned long x, const unsigned long *dp)
{
  int8_t c;
  unsigned long d;

  if (x) {
    while (x < *dp) {
      ++dp;
    }
    do {
      d = *dp++;
      c = '0';
      while (x >= d) ++c, x -= d;
      bb_put_byte(c);
    }
    while (!(d & 1));
  } else {
    bb_put_byte('0');
  }
}

#if defined(BB_PRINTF_HEX_SUPPORT)
void
bb_put_hex(unsigned n)
{
  static const int8_t hex[16] = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A','B','C','D','E','F'
  };
  bb_put_byte(hex[n & 15]);
}
#endif /* BB_PRINTF_HEX_SUPPORT */

void
bb_vprintf(const char* format, va_list a)
{
  int8_t c;
  int i;
#if defined(BB_PRINTF_LONG_SUPPORT)
  long n;
#endif

  while ((c = *format++)) {
    if (c == '%') {
      switch ((c = *format++)) {
#if defined(BB_PRINTF_STRING_SUPPORT)
      case 's': /* string */
        bb_put_string(va_arg(a, char*));
        break;
#endif /* BB_PRINTF_STRING_SUPPORT */
      case 'c': /* character */
        bb_put_byte((char)va_arg(a, int)); /* char? */
        break;
      case 'd': /* '%d' and '%i' are synonymous for output */
      case 'i': /* 16 bit integer */
      case 'u': /* 16 bit unsigned */
        i = va_arg(a, int);
        if (c == 'i' && i < 0) {
          i = -i;
          bb_put_byte('-');
        }
        xtoa((unsigned)i, dv + 5);
        break;
#if defined(BB_PRINTF_LONG_SUPPORT)
      case 'l': /* 32 bit long */
      case 'n': /* 32 bit unsigned long */
        n = va_arg(a, long);
        if (c == 'l' &&  n < 0) {
          n = -n;
          bb_put_byte('-');
        }
        xtoa((unsigned long)n, dv);
        break;
#endif /* BB_PRINTF_LONG_SUPPORT */
#if defined(BB_PRINTF_HEX_SUPPORT)
      case 'x': /* 16 bit hexadecimal */
        i = va_arg(a, int);
        bb_put_hex(i >> 12);
        bb_put_hex(i >> 8);
        bb_put_hex(i >> 4);
        bb_put_hex(i);
        break;
#endif /* BB_PRINTF_HEX_SUPPORT */
      case 0:
        return;
      case '%':
        bb_put_byte('%');
        break;
      default:
        goto bad_fmt;
      }
    } else {
    bad_fmt: bb_put_byte(c);
    }
  }
}

void
bb_printf(const char* format, ...)
{
  va_list a;
  va_start(a, format);
  bb_vprintf(format, a);
  va_end(a);
}

/* TODO(team): please revise the following statement. */
/*
 * Hub address of global lock that all cogs will share. This address
 * has to be reserved and initialized (see propeller_locknew()) by
 * multicog bootloader.
 */
#define SIO_COGSAFE_LOCK_ADDR (int16_t*)0x7530

#ifdef SIO_COGSAFE_PRINTING
static int16_t cogsafe_lock;
#endif

void
bb_sio_init()
{
  DIR_OUTPUT(SIO_TX_PIN);
  //BBOS_DELAY_MSEC(1);
#ifdef SIO_COGSAFE_PRINTING
  cogsafe_lock = *SIO_COGSAFE_LOCK_ADDR;
  if (cogsafe_lock == 0) {
    cogsafe_lock = propeller_locknew();
    *(SIO_COGSAFE_LOCK_ADDR) = cogsafe_lock + 1;
    propeller_lockclr(cogsafe_lock);
  } else {
    cogsafe_lock = cogsafe_lock - 1;
  }
#endif /* SIO_COGSAFE_PRINTING */
}

/* Note, the current implementation allows SIO_COGSAFE_PRINTING
   to permanently reserve one lock (see locknew()). */
#ifdef SIO_COGSAFE_PRINTING

void
sio_cogsafe_printf(const char* format, ...)
{
  va_list a;
  while (propeller_lockset(cogsafe_lock)); /* wait until we lock sio */
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  propeller_lockclr(cogsafe_lock); /* unlock sio */
}
#endif /* SIO_COGSAFE_PRINTING */

#ifdef SIO_LOCK_PRINTING
void
sio_lock_printf(int lock, const char* format, ...)
{
  va_list a;
  while (propeller_lockset(lock)); /* wait until we lock the serial */
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  propeller_lockclr(lock); /* unlock the serial */
}

#endif /* SIO_LOCK_PRINTING */
