/*
 * Copyright (c) 2011 Sladeware LLC
 *
 * This implementation is only support Catalina compiler.
 * See the following link to learn more about initial implementation:
 * http://forums.parallax.com/showthread.php?128947-Catalina-2.9/page21
 *
 * Read more about serial communication:
 * http://en.wikipedia.org/wiki/Asynchronous_serial_communication
 */

/* Please keep the following checkpoint for driver safety, so it wan't be
   included directly by application. */
#ifndef OK
#error not OK
#endif

/* The following implementation supports only Catalina compiler interface. */
#ifndef __CATALINA__
#error "This implementation required Catalina Compiler"
#endif

#include <catalina_cog.h>

//#include <bb/os/drivers/gpio/p8x32_gpio.h>
//#include BBOS_PROCESSOR_FILE(time.h)

/* Created with spin.binary PASM to C Array Converter. */
unsigned int serial_cog[] = {
  0xa0bca9f0, 0x80fca810, 0x08bcaa54, 0xa0fcb201,
  0x2cbcb255, 0x80fca804, 0x08bcaa54, 0xa0fcbe01,
  0x2cbcbe55, 0x80fca804, 0x08bcae54, 0x80fca804,
  0x08bcb054, 0x80fca804, 0x08bcb454, 0xa0bcc05a,
  0x80fcc010, 0x627cae04, 0x617cae02, 0x689be85f,
  0x68abec5f, 0xa0fcc833, 0x5cbcbc64, 0x627cae01,
  0x613cb3f2, 0x5c640016, 0xa0fcb809, 0xa0bcba58,
  0x28fcba01, 0x80bcbbf1, 0x80bcba58, 0x5cbcbc64,
  0xa0bca85d, 0x84bca9f1, 0xc17ca800, 0x5c4c001f,
  0x613cb3f2, 0x30fcb601, 0xe4fcb81e, 0x28fcb617,
  0x60fcb6ff, 0x627cae01, 0x6cd4b6ff, 0x08bcabf0,
  0x80bcaa5a, 0x003cb655, 0x84bcaa5a, 0x80fcaa01,
  0x60fcaa0f, 0x083cabf0, 0x5c7c0016, 0x5cbcc85e,
  0xa0bca9f0, 0x80fca808, 0x08bcaa54, 0x80fca804,
  0x08bcac54, 0x863caa56, 0x5c680033, 0x80bcac60,
  0x00bcc256, 0x84bcac60, 0x80fcac01, 0x60fcac0f,
  0x083cac54, 0x68fcc300, 0x2cfcc202, 0x68fcc201,
  0xa0fcc40b, 0xa0bcc7f1, 0x627cae04, 0x617cae02,
  0x6ce0c201, 0x29fcc201, 0x70abe85f, 0x7497ec5f,
  0x80bcc658, 0x5cbcc85e, 0xa0bca863, 0x84bca9f1,
  0xc17ca800, 0x5c4c004d, 0xe4fcc446, 0x5c7c0033
};

/**
 * Defines serial  structure.
 * 9 contiguous longs + buffers
 */
typedef struct serial_config {
  uint32_t rx_head;    /* receive queue head */
  uint32_t rx_tail;    /* receive queue tail */
  uint32_t tx_head;    /* transmit queue head */
  uint32_t tx_tail;    /* transmit queue tail */
  uint32_t rx_pin;     /* recieve pin */
  uint32_t tx_pin;     /* transmit pin */
  uint32_t mode;       /* interface mode */
  uint32_t bit_ticks;  /* clkfreq / baudrate */
  uint32_t buffer_ptr; /* pointer to rx buffer */
} serial_config_t;

/* Serial config instance */
static struct serial_config config;

/**
 * These buffers must be contiguous. Their size must match the asm expectation.
 * Asm also expects the address of @c txbuff to be after @c rxbuff.
 * Apparently the C compiler "allocates" this memory in reverse order.
 * Using a struct would correct it, but for now let's just reverse the entry.
 */
static int8_t serial_buff[16];

void
serial_open(bbos_device_id_t dev_id, uint32_t rx_pin, uint32_t tx_pin, 
    uint32_t mode, uint32_t baudrate)
{
  config.rx_head = 0; /* rx_head */
  config.rx_tail = 0; /* rx_tail */
  config.tx_head = 0; /* tx_head */
  config.tx_tail = 0; /* tx_tail */
  config.rx_pin = rx_pin;
  config.tx_pin = tx_pin;
  config.mode = mode;
  config.bit_ticks = _clockfreq() / baudrate;
  config.buffer_ptr = (uint32_t)&serial_buff[0];
  _coginit((int)&serial_descr >> 2, (int)serial_cog >> 2, ANY_COG);
}

/* Transmit a set of bytes */
void
serial_transmit(int8_t* buf, size_t sz)
{
  int i;
  int echo;
    
  for (i = 0; i < sz; i++)
    {
      echo = serial_transmit_byte(buf[i]);
    }
}

/**
 * Transmit a single byte on the transmit queue.
 * @param byte Byte to send.
 *
 * @return
 * Return echo if SERIAL_MODE_IGNORE_TX_ECHO or -1.
 */
int
serial_send_byte(int byte)
{
  int echo = -1;

  /* wait if the head has looped right round and is now
     one less than the tail */
  while (config.tx_tail == ((config.tx_head + 1) & SERIAL_BUFF_MASK));

  serial_buff[SERIAL_BUFF_MASK + 1 + config.tx_head] = byte;
  config.tx_head = (config.tx_head + 1) & SERIAL_BUFF_MASK;

  if (config.mode & SERIAL_MODE_IGNORE_TX_ECHO)
    {
      /* why not check or timeout... this blocks for char */
      echo = serial_receive_byte();
    }

  return echo;
}

/**
 * Gets a byte from the receive queue if available. Note, that function does 
 * not block. We move rx_tail after getting char.
 *
 * @returns
 * Receive byte 0 to 0xff or -1 if none available.
 */
int
serial_wait()
{
  int byte = -1;

  if(config.rx_tail != config.rx_head)
    {
      byte = serial_buff[config.rx_tail];
      config.rx_tail = (config.rx_tail + 1) & SERIAL_BUFF_MASK;
    }

  return byte;
}

/* Receive a sequence of bytes. Wait until all the bytes will be received. */
void
serial_receive(int8_t* buf, size_t sz)
{
  size_t i;
  
  for (i = 0; i < sz; i++)
    {
      buf[i] = serial_receive_byte();
    }
}

/**
 * Wait for a byte from the receive queue. Blocks until something is ready.
 *
 * @returns
 * Received byte.
 */
int
serial_receive_byte()
{
  int byte;

  while ((byte = serial_wait()) < 0);

  return byte;
}

/* Flush receive buffer. */
void
serial_flush()
{
  while (serial_wait() != -1); /* keep checking until buffer clear */
}

/**
 * Wait ms milliseconds for byte, -1 if nothing.
 */
int
serial_timeout(uint32_t ms)
{
  int byte = -1;
  int t0 = 0;
  int t1 = 0;

  t0 = _cnt();
  do
    {
      byte = serial_wait();
      t1 = _cnt();
      if (((t1 - t0) / (_clockfreq() / 1000)) > ms)
        {
          break;
        }
      } while(byte < 0);

  return byte;
}

