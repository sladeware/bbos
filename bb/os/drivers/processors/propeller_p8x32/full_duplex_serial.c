/*
 * Copyright (c) 2012 Slade Maurer, Alexander Sviridenko
 */

#include <catalina_cog.h>
#include "full_duplex_serial.h"
#include "bitwise_op.h"

struct {
  /* Receiving */
  uint32_t rx_pin;
  uint32_t rx_head;
  uint32_t rx_tail;
  char* rx_buffer;
  /* Transmission */
  uint32_t tx_pin;
  uint32_t tx_head;
  uint32_t tx_tail;
  char* tx_buffer;
  uint32_t mode;
  uint32_t bit_ticks;
} config;

/* The rx and tx buffers must be contiguous. */
char rx_buffer[256];
char tx_buffer[256];

void
full_duplex_serial_open(uint32_t rx_pin, uint32_t tx_pin,
                        uint32_t mode, uint32_t baudrate)
{
  config.rx_pin = rx_pin;
  config.tx_pin = tx_pin;

  config.mode = mode;
  config.bit_ticks = _clockfreq() / baudrate;

  config.rx_head = config.rx_tail = 0;
  config.rx_buffer = rx_buffer;
  config.tx_head = config.tx_tail = 0;
  config.tx_buffer =tx_buffer;

  /* Initialize tx pin according to mode */
  if (!(config.mode & SERIAL_MODE_OPENDRAIN_TX) != is_odd(config.mode & SERIAL_MODE_INVERT_TX))
    {
      _outa(1 << tx_pin, 1 << tx_pin);
    }
  if (!(config.mode & SERIAL_MODE_OPENDRAIN_TX))
    {
      _dira(1 << tx_pin, 1 << tx_pin);
    }
}

void
full_duplex_serial_send_byte(char byte)
{
  int frame;
  unsigned i;
  unsigned cnt;
  uint32_t pin;
  uint32_t bitticks;

  pin = config.tx_pin;
  bitticks = config.bit_ticks;
  /* Ready byte to transmit */
  frame = 0x400 | (byte << 2) | 1; /* [1|x|x|x|x|x|x|x|x|0|1] */

  /* Transmit the frame */
  cnt = _cnt();
  i = 11;

  if (!(config.mode & SERIAL_MODE_OPENDRAIN_TX))
    {
      for (i = 11; i > 0; i--)
        {
          _outa(1 << pin, (frame & 1) << pin);
          frame >>= 1; /* move to the next bit */
          cnt += bitticks; /* ready next bit period */
          while (cnt > _cnt()); /* check if bit transmit period done */
          /* go for another bit to transmit */
        }
    }
  else
    {
      for (i = 11; i > 0; i--)
        {
          _dira(1 << pin, (!(frame & 1)) << pin);
          frame >>= 1; /* move to the next bit */
          cnt += config.bit_ticks; /* ready next bit period */
          while (cnt > _cnt()); /* check if bit transmit period done */
          /* go for another bit to transmit */
        }
    }
}

/**
 * Wait for a byte from the receive queue. Blocks until something is ready.
 *
 * @returns
 * Received byte.
 */
int
full_duplex_serial_wait_byte()
{
  int byte;
  while ((byte = full_duplex_serial_receive_byte()) < 0);
  return byte;
}

/**
 * Gets a byte from the receive queue if available. Note, that function does
 * not block. We move rx_tail after getting char.
 *
 * @returns
 * Receive byte 0 to 0xFF or -1 if none available.
 */
int
full_duplex_serial_receive_byte()
{
  int byte = -1;
  char rx_bits;
  unsigned rx_cnt;
  int rx_data = 1;

  /* wait for start bit on rx pin */
  //while ((config.mode & SERIAL_MODE_INVERT_RX)
  //       && is_odd(_ina() & config.rx_mask));

  /* ready to receive a byte */
  rx_cnt = (config.bit_ticks >> 1) + _cnt();
  for (rx_bits = 9; rx_bits > 0; rx_bits--)
    {
      rx_cnt += config.bit_ticks; /* ready next bit period */

      while (rx_cnt >= _cnt()); /* check if bit receive period done */

      /* receive bit on rx pin */
      rx_data = rcr(rx_data, 1, is_odd(_ina() & (1 << config.rx_pin)));
    }

  rx_data >>= 32 - 9; /* justify and ... */
  rx_data &= 0xFF;    /* ... trim received byte */

  /* if rx inverted, invert byte */
  if (config.mode & SERIAL_MODE_INVERT_RX)
    {
      rx_data ^= 0xFF;
    }

  /* save received byte and increase head */
  *(config.rx_buffer + config.rx_head) = rx_data;
  config.rx_head = (config.rx_head + 1) & 0xFF;

  //if(config.rx_tail != config.rx_head)
  //  {
  //    byte = config.rx_buffer[config.rx_tail];
  //    config.rx_tail = (config.rx_tail + 1) & 0xFF;
  //  }

  return rx_data; //byte;
}
