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

/**
 * Note, sio_put_char() and sio_get_char() is the only external dependency
 * for this file.
 */

#include <bb/os/drivers/processors/propeller_p8x32/sio.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>
#include <stdarg.h>

#define SIO_PRINTF_STRING_SUPPORT
#define SIO_COGSAFE_PRINTING

/**
 * Receive a character to serial.
 *
 * @return
 *
 * 8-bit character.
 */
int8_t
sio_get_char()
{
  int32_t rx_data;
  uint32_t num_bitticks;
  uint32_t bitticks_cnt;
  int8_t i;

  /* Initialization */
  i = 8;
  rx_data = 0;
  num_bitticks = propeller_get_clockfreq() / SIO_BAUDRATE;

  /* wait for start bit on rx pin */
  while (GET_INPUT(SIO_RX_PIN));

  /* ready to receive a byte */
  bitticks_cnt = propeller_get_cnt() + (num_bitticks >> 1);
  /* start receiving */
  do
    {
      bitticks_cnt += num_bitticks; /* ready next bit period */
      /* check if bit receive period done */
      while (bitticks_cnt > propeller_get_cnt());
      /* put the next bit */
      rx_data >>= 1;
      rx_data = rx_data &~ GET_MASK(SIO_RX_PIN);
      rx_data |= GET_INPUT(SIO_RX_PIN) << SIO_RX_PIN;/* receive bit on rx pin */
    } while (i--);

  /* Enrolled version of the while-loop above. */
#if 0
#define RECEIVE_BIT                                                     \
  do {                                                                  \
    bitticks_cnt += num_bitticks;                                       \
    while (bitticks_cnt > propeller_get_cnt());                         \
    rx_data = rx_data &~ GET_MASK(SIO_RX_PIN);                          \
    rx_data |= GET_INPUT(SIO_RX_PIN) << SIO_RX_PIN;                     \
    rx_data >>= 1;                                                      \
  } while (0)

  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
  RECEIVE_BIT;
#endif

  /* justify (32 - 9) and trim received byte */
  rx_data = (rx_data >> 23) & 0xFFFF;

  return (int8_t)rx_data;
}

/**
 * Writes a character to the serial. This function is safe to changing
 * of clock frequency.
 */
void
sio_put_char(int8_t c)
{
  int frame;
  uint32_t bitticks_cnt;
  uint32_t num_bitticks;

  /* Initialize tx pin */
  DIR_OUTPUT(SIO_TX_PIN);

  /* Ready character byte to transmit */
  frame = 0x400 | (c << 2) | 1; /* Frame format: 1 _ _ _ _ _ _ _ _ 0 1 */

  num_bitticks = propeller_get_clockfreq() / SIO_BAUDRATE;
  bitticks_cnt = propeller_get_cnt();

  /* XXX: the following code can be enrolled in while-loop or
     for-statement.*/
#define TRANSMIT_BIT                                                    \
  do {                                                                  \
    OUT_TO(SIO_TX_PIN, (frame & 1));                                    \
    frame >>= 1; /* move to the next bit */                             \
    bitticks_cnt += num_bitticks; /* ready next bit period */           \
    while (bitticks_cnt > propeller_get_cnt()); /* ensure that bit transmit period done */ \
  } while (0)

  /* Transmit the frame bits one by one*/
  TRANSMIT_BIT;
  /* Actual 8-bit data */
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
}

#if defined(SIO_PRINTF_STRING_SUPPORT)
void
sio_put_string(int8_t* s)
{
  while (*s)
    {
      sio_put_char(*s++);
    }
}
#endif /* SIO_PRINTF_STRING_SUPPORT */

static const unsigned long dv[] = {
//  4294967296      // 32 bit unsigned max
    1000000000,     // +0
     100000000,     // +1
      10000000,     // +2
       1000000,     // +3
        100000,     // +4
//       65535      // 16 bit unsigned max
         10000,     // +5
          1000,     // +6
           100,     // +7
            10,     // +8
             1,     // +9
};

static void
xtoa(unsigned long x, const unsigned long *dp)
{
  int8_t c;
  unsigned long d;

  if (x)
    {
      while (x < *dp)
        {
          ++dp;
        }
      do
        {
          d = *dp++;
          c = '0';
          while (x >= d) ++c, x -= d;
          sio_put_char(c);
        }
      while (!(d & 1));
    }
  else
    {
      sio_put_char('0');
    }
}

#if defined(SIO_PRINTF_HEX_SUPPORT)
void
sio_put_hex(unsigned n)
{
  static const int8_t hex[16] = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A','B','C','D','E','F'
  };
  sio_put_char(hex[n & 15]);
}
#endif /* SIO_PRINTF_HEX_SUPPORT */

static void
_sio_multiarg_printf(const int8_t* format, va_list a)
{
  int8_t c;
  int i;
#if defined(SIO_PRINTF_LONG_SUPPORT)
  long n;
#endif

  while ((c = *format++))
    {
      if (c == '%')
        {
          switch ((c = *format++)) {
#if defined(SIO_PRINTF_STRING_SUPPORT)
          case 's': /* string */
            sio_put_string(va_arg(a, int8_t*));
            break;
#endif /* SIO_PRINTF_STRING_SUPPORT */
          case 'c': /* character */
            sio_put_char((int8_t)va_arg(a, int)); /* char? */
            break;
          case 'd': /* '%d' and '%i' are synonymous for output */
          case 'i': /* 16 bit integer */
          case 'u': /* 16 bit unsigned */
            i = va_arg(a, int);
            if (c == 'i' && i < 0)
              {
                i = -i;
                sio_put_char('-');
              }
            xtoa((unsigned)i, dv + 5);
            break;
#if defined(SIO_PRINTF_LONG_SUPPORT)
          case 'l':                /* 32 bit long */
          case 'n':                /* 32 bit unsigned long */
            n = va_arg(a, long);
            if (c == 'l' &&  n < 0)
              {
                n = -n;
                sio_put_char('-');
              }
            xtoa((unsigned long)n, dv);
            break;
#endif /* SIO_PRINTF_LONG_SUPPORT */
#if defined(SIO_PRINTF_HEX_SUPPORT)
          case 'x': /* 16 bit hexadecimal */
            i = va_arg(a, int);
            sio_put_hex(i >> 12);
            sio_put_hex(i >> 8);
            sio_put_hex(i >> 4);
            sio_put_hex(i);
            break;
#endif /* SIO_PRINTF_HEX_SUPPORT */
          case 0:
            return;
          case '%':
            sio_put_char('%');
            break;
          default:
            goto bad_fmt;
          }
        }
      else
        {
        bad_fmt: sio_put_char(c);
        }
    }
}

/**
 * See http://en.wikipedia.org/wiki/Printf#Format_placeholders
 */
void
sio_printf(const int8_t* format, ...)
{
  va_list a;
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
}

/*******************************
 * Lock safe printing routines *
 *******************************/

/*
 * Note, the current implementation allows SIO_COGSAFE_PRINTING
 * to permanently reserve one lock (see locknew()).
 */
#ifdef SIO_COGSAFE_PRINTING
/** Hub address of global lock that all cogs will share. This address
 * has to be reserved and initialized (see locknew()) by multicog
 * bootloader.
 */
#define SIO_COGSAFE_LOCK_ADDR (int*)0x61A8

void
sio_cogsafe_printf(const int8_t* format, ...)
{
  va_list a;
  while (*SIO_COGSAFE_LOCK_ADDR); /* wait until we lock the serial */
  *SIO_COGSAFE_LOCK_ADDR = 1;
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  *SIO_COGSAFE_LOCK_ADDR = 0; /* unlock the serial */
}
#endif /* MULTICOG_SAFE_PRINTING */

#ifdef SIO_LOCK_PRINTING
/**
 * Lock printing routine. This routine assumes that _locknew() was
 * used before.
 */
void
sio_lock_printf(int lock, const int8_t* format, ...)
{
  va_list a;
  while (propeller_lockset(lock)); /* wait until we lock the serial */
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  propeller_lockclr(lock); /* unlock the serial */
}

#endif /* SIO_LOCK_PRINTING */
