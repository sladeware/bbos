/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include "types.h"
#include "sio.h"
#include <stdarg.h>

/* Special settings for catalina compiler */
#ifdef __CATALINA__
#define SIO_RX_PIN       31 /* SI_PIN   */
#define SIO_TX_PIN       30 /* SO_PIN   */
#define SIO_BAUDRATE 115200 /* SIO_BAUD */
#endif

/**
 * Writes a character to the serial. This function is safe to changing
 * of clock frequency.
 *
 * sio_put_char() is the only external dependency for this file.
 *
 * @see full_duplex_serial.h for more details.
 */
void
sio_put_char(char c)
{
  int frame;
  uint32_t bitticks_cnt;
  uint32_t num_bitticks;

  /* Initialize tx pin */
  _dira(1 << SIO_TX_PIN, 1 << SIO_TX_PIN);

  /* Ready character byte to transmit */
  frame = 0x400 | (c << 2) | 1; /* Frame format: 1 _ _ _ _ _ _ _ _ 0 1 */

  num_bitticks = _clockfreq() / SIO_BAUDRATE;
  bitticks_cnt = _cnt();

  /* XXX: the following code can be enrolled in while-loop or
     for-statement.*/
#define TRANSMIT_BIT                                                    \
  do {                                                                  \
    _outa(1 << SIO_TX_PIN, (frame & 1) << SIO_TX_PIN);                  \
    frame >>= 1; /* move to the next bit */                             \
    bitticks_cnt += num_bitticks; /* ready next bit period */           \
    _waitcnt(bitticks_cnt); /* ensure that bit transmit period done */  \
  } while (0)

  /* Transmit the frame bits one by one*/
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
}

void
sio_put_string(char* s)
{
  while (*s)
    {
      sio_put_char(*s++);
    }
}

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
  char c;
  unsigned long d;

  if (x)
    {
      while (x < *dp)
        ++dp;
      do
        {
          d = *dp++;
          c = '0';
          while(x >= d) ++c, x -= d;
          sio_put_char(c);
        }
      while(!(d & 1));
    }
  else
    {
      sio_put_char('0');
    }
}

void
sio_put_hex(unsigned n)
{
  static const char hex[16] = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A','B','C','D','E','F'
  };
  sio_put_char(hex[n & 15]);
}

static void
_sio_multiarg_printf(const char* format, va_list a)
{
  char c;
  int i;
  long n;

  while (c = *format++)
    {
      if (c == '%')
        {
          switch(c = *format++) {
          case 's':                /* string */
            sio_put_string(va_arg(a, char*));
            break;
          case 'c':                /* character */
            sio_put_char(va_arg(a, char));
            break;
          case 'd':                /* '%d' and '%i' are synonymous for output */
          case 'i':                /* 16 bit integer */
          case 'u':                /* 16 bit unsigned */
            i = va_arg(a, int);
            if (c == 'i' && i < 0)
              {
                i = -i;
                sio_put_char('-');
              }
            xtoa((unsigned)i, dv + 5);
            break;
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
          case 'x':                /* 16 bit hexadecimal */
            i = va_arg(a, int);
            sio_put_hex(i >> 12);
            sio_put_hex(i >> 8);
            sio_put_hex(i >> 4);
            sio_put_hex(i);
            break;
          case 0:
            return;
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
sio_printf(const char* format, ...)
{
  va_list a;
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
}

/*
 * Lock safe printing routines.
 */

/*
 * Note, the current implementation allows SIO_COGSAFE_PRINTING
 * to permanently reserve one lock (see locknew()).
 */
#ifdef SIO_COGSAFE_PRINTING

/** Hub address of global lock that all cogs will share. This address
 * has to be reserved and initialized (see locknew()) by multicog
 * bootloader.
 */
static int* sio_cogsafe_lock_addr = 0;

void
sio_cogsafe_printf(const char* format, ...)
{
  va_list a;
  int lock_id;
  lock_id = *multicog_lock_addr;
  while (_lockset(lock_id)); /* wait until we lock the serial */
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  _lockclr(lock_id); /* unlock the serial */
}

#endif /* MULTICOG_SAFE_PRINTING */

#ifdef SIO_LOCK_PRINTING
/**
 * Lock printing routine. This routine assumes that _locknew() was
 * used before.
 */
void
sio_lock_printf(int lock, const char* format, ...)
{
  va_list a;
  while (_lockset(lock)); /* wait until we lock the serial */
  va_start(a, format);
  _sio_multiarg_printf(format, a);
  va_end(a);
  _lockclr(lock); /* unlock the serial */
}

#endif /* SIO_LOCK_PRINTING */
