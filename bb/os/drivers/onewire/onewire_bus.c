/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/os/drivers/onewire/onewire_bus.h>

/* Delay values are in microseconds */
#define RESET_DELAY 480
#define DIR_DELAY 72
#define INPUT_DELAY 428
#define RECOVERY_DELAY 2
#define WUFF_DELAY 12
#define END_DELAY (60 - 15)
uint8_t
ow_input_pin_state(uint8_t pin)
{
  return OW_GET_INPUT(pin);
}

/**
 * @return
 *
 * Error
 */
uint8_t
ow_reset(uint8_t pin)
{
  uint8_t err;
  /* Pull bus low */
  OW_OUT_LOW(pin); /* disable internal pull-up (can be on from parasite) */
  OW_DIR_OUTPUT(pin); /* pull OW-Pin low for 480us */
  ow_delay_usec(RESET_DELAY); /* Wait for some time */
  /* Release bus */
  OW_DIR_INPUT(pin); /* set Pin as input - wait for clients to pull low */
  ow_delay_usec(DIR_DELAY);
  /* Sample data */
  err = OW_GET_INPUT(pin); /* no presence detect */
  /* After a delay the clients should release the line
   * and input-pin gets back to high due to pull-up-resistor */
  ow_delay_usec(INPUT_DELAY);
  if(OW_GET_INPUT(pin) == 0) /* short circuit */
    {
      err = 1;
    }
  return err;
}

uint8_t
ow_io_bit(uint8_t bit, uint8_t pin)
{
  OW_DIR_OUTPUT(pin); /* drive bus low */
  ow_delay_usec(RECOVERY_DELAY); // Recovery-Time wuffwuff was 1
  if (bit)
    {
      OW_DIR_INPUT(pin); /* if bit is 1 set bus high (by ext. pull-up) */
    }

  /* wuff-wuff delay was 15uS-1 see comment above */
  /* ow_delay_usec(WUFF_DELAY); */ /* !!! */

  if (OW_GET_INPUT(pin) == 0)
    {
      bit = 0;  /* sample at end of read-timeslot */
    }
  ow_delay_usec(END_DELAY);
  OW_DIR_INPUT(pin);
  return bit;
}

uint8_t
ow_io_byte(uint8_t byte, uint8_t pin)
{
  uint8_t i = 8, j;
  do
    {
      j = ow_io_bit(byte & 1, pin);
      byte >>= 1;
      if (j)
        {
          byte |= 0x80;
        }
    }
  while (--i);
  return byte;
}

void
ow_command(uint8_t cmd, uint8_t pin)
{
  ow_reset(pin);
  /* To all devices */
  ow_write_byte(OW_SKIP_ROM, pin);
  ow_write_byte(cmd, pin);
}
