/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bbos/hardware/drivers/onewire/slaves/ds18b20.c
 * @brief DS18B20 temp sensor
 */

#include <bbos.h>
#include <bbos/drivers/onewire/slaves/ds18b20.h>
#include <bbos/drivers/onewire/bus.h>

void
ds18b20_meas_to_cel(unsigned char *sp)
{
	unsigned int meas;
	unsigned char i;
	unsigned char t;
	unsigned int diff;

	meas = sp[0]; // LSB
	meas |= ((unsigned int)sp[1]) << 8; // MSB
	
	t = (unsigned char)(meas >> 4);
	printf("Temperature: %dC\n", t);


	diff = t-27;
	
	for (i=0; i<8; i++) {
		if(i <= diff) {
			_outa(1<<(16+i), 1<<(16+i));
			_dira(1<<(16+i), 1<<(16+i));
		} else {
			_outa(1<<(16+i), 0);
			_dira(1<<(16+i), 0);
		}
	}
	
	if (t == 30) {
		_outa(1<<7, 1<<7);
		_dira(1<<7, 1<<7);
	} else {
		_outa(1<<7, 0);
		_dira(1<<7, 0);
	}
}

/**
 * Read temperature (scratchpad) of sensor.
 */
static uint8_t
ds18b20_read_data()
{
	uint8_t i;
	uint8_t sp[DS18B20_SCRATCHPAD_SIZE];

	ow_reset();

	ow_command(DS18B20_READ_SCRATCHPAD);

	for (i=0; i<DS18B20_SCRATCHPAD_SIZE; i++) {
		sp[i] = ow_read_byte();
	}
		
	ds18b20_meas_to_cel(sp);
}

/** Start measurement for all sensors. */
static uint8_t
ds18b20_request_data()
{
	ow_reset();
	
	/*
	 * Now we need to read the state from the input pin to define whether the bus 
	 * is "idle".
	 */
	if (ow_input_pin_state()) {
		ow_command(DS18B20_CONVERT_TEMPERATURE);
		return 0;
	}
	
	return 0xFF;
}

/**
 * DS18B20 driver thread.
 */
void
ds18b20_driver()
{
}



