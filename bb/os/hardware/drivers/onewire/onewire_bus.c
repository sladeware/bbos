/*
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bbos.h>
#include <bbos/drivers/onewire/bus.h>

static unsigned ow_dpin = 1<<0;

uint8_t
ow_input_pin_state() {
	return OW_GET_INPUT();
}

/**
 * @return
 *
 * Error.
 */
uint8_t
ow_reset()
{
	uint8_t err;

	/* Pull bus low */
	OW_OUT_LOW(); // disable internal pull-up (can be on from parasite)
	OW_DIR_OUTPUT(); // pull OW-Pin low for 480us
	
	/* Wait for some time */
	ow_delay_usec(480);
	
	/* Release bus */
	OW_DIR_INPUT(); // set Pin as input - wait for clients to pull low
	
	ow_delay_usec(72);
	
	/* Sample data */
	err = OW_GET_INPUT(); // no presence detect

	/* After a delay the clients should release the line
	 * and input-pin gets back to high due to pull-up-resistor */
	ow_delay_usec(428);
	
  if(OW_GET_INPUT() == 0) // short circuit
   err = 1;

	return err;
}

uint8_t
ow_io_bit(uint8_t bit)
{
	OW_DIR_OUTPUT(); // drive bus low

	ow_delay_usec(2); // Recovery-Time wuffwuff was 1
  if (bit) {
  	OW_DIR_INPUT(); // if bit is 1 set bus high (by ext. pull-up)
  }

	// wuffwuff delay was 15uS-1 see comment above
	//ow_delay_usec(12); // !!!

	if (OW_GET_INPUT() == 0)
		bit = 0;  // sample at end of read-timeslot

	ow_delay_usec(60-15);

	OW_DIR_INPUT();

	return bit;
}

uint8_t
ow_io_byte(uint8_t byte)
{
	uint8_t i = 8, j;

	do {
		j = ow_io_bit(byte & 1);
		byte >>= 1;
		if (j) {
			byte |= 0x80;
		}
	} while (--i);

	return byte;
}

void
ow_command(uint8_t cmd)
{
	ow_reset();
	
	// To all devices
	ow_write_byte(OW_SKIP_ROM);

	ow_write_byte(cmd);
}





