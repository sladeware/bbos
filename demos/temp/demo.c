/*
 * DS18B20 Demo.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

long usec_delay;

void
bbos_time_init()
{
	usec_delay = (_clockfreq() + 999999) / 1000000;
}

#include <catalina_cog.h>
#include <catalina_hmi.h>
#include <bbos/drivers/onewire/slaves/ds18b20.h>

#define TEST_FREQ 5000000
#define TEST_MODE XTAL_1 + PLL16X

void
main()
{
	//_clockinit(TEST_MODE, TEST_FREQ);
	printf("Current frequency = %u\n", _clockfreq);

	bbos_time_init();

	while (1) {
		ds18b20_request_data();
		ds18b20_read_data();
	
		_waitcnt(_cnt() + _clockfreq() / 3);
	}
}


