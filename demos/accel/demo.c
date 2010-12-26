/*
 * Hitachi H48C 3 Axis Accelerometer Demo.
 *
 * Copyright (c) Slade Maurer, Alexander Sviridenko
 */

#include <bbos/kernel.h>
#include <bbos/kernel/time.h>
#include <catalina_cog.h>
#include <catalina_hmi.h>

#include <bbos/drivers/accel/h48c.h>

#define TEST_FREQ 5000000
#define TEST_MODE XTAL_1 + PLL16X

int gforce_x, gforce_y, gforce_z;
int32_t h48c_theta_a, h48c_theta_b, h48c_theta_c;

long usec_delay;

void
bbos_time_init()
{
	usec_delay = (_clockfreq() + 999999) / 1000000;
}

void
main()
{
	_clockinit(TEST_MODE, TEST_FREQ);
	printf("Current frequency = %u\n", _clockfreq);

	bbos_time_init();

	h48c_open(1, 2, 0, 3);

	while (1)
	{
		gforce_x = h48c_gforce_of_axis(H48C_SELECT_AOX);
		gforce_y = h48c_gforce_of_axis(H48C_SELECT_AOY);
		gforce_z = h48c_gforce_of_axis(H48C_SELECT_AOZ);
	
		printf("G-XYZ [%d, %d, %d]\n", gforce_x, gforce_y, gforce_z);

		if (h48c_free_fall())
		{
			_outa(0xFF0000, 0xFF0000);
			_dira(0xFF0000, 0xFF0000);
		}
		else {
			_outa(0xFF0000, 0);
			_dira(0xFF0000, 0);
		}

//		_waitcnt(_cnt() + _clockfreq() / 2);
	}
	
	return;
}


