/*
 * Hitachi H48C 3 Axis Accelerometer Driver.
 *
 * The Hitachi H48C Tri-Axis Accelerometer is an integrated module that can 
 * sense gravitational (g) force of ±3g on three axes (X, Y, and Z). The module 
 * contains an onboard regulator to provide 3.3-volt power to the H48C, analog 
 * signal conditioning, and an MCP3204 (four channel, 12-bit) analog-to-digital 
 * onverter to read the H48C voltage outputs. Acquiring measurements from the 
 * module is simplified through a synchronous serial interface. 
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/kernel.h>
#include <stdio.h>
#include <bbos/drivers/accel/h48c.h>
#include <catalina_cog.h>
#include <catalina_hmi.h>
#include <bbos/kernel/math/unsigned.h>

#define PIN(p) (1<<p)
#define SET_HIGH(p) _outa(PIN(p), PIN(p))
#define SET_LOW(p) _outa(PIN(p), 0)
#define SET_OUTPUT(p) _dira(PIN(p), PIN(p))

/*
 *        +---------+
 * CLK -- | 1 o   6 | -- Vdd (+5V)
 * DIO -- | 2     5 | -- CS
 * Vss -- | 3     4 | -- Zero-G
 *        +---------+
 *
 * Pin definitions:
 *
 * CLK    : Synchronous clock input
 * DIO    : Bi-directional data to/from host
 * Vss    : Power supply ground
 * Zero-G : "Free-fall" output; active-high
 * CSS    : Chip select input; active-low
 * Vdd    : +5V
 */

long table[] = { 
	0x20000000, 0x12E4051E, 0x09FB385B, 0x051111D4, 0x028B0D43,
	0x0145D7E1, 0x00A2F61E, 0x00517C55, 0x0028BE53, 0x00145F2F,
  0x000A2F98, 0x000517CC, 0x00028BE6, 0x000145F3, 0x0000A2FA,
  0x0000517D, 0x000028BE, 0x0000145F, 0x00000A30, 0x00000518
};

#define COUNTS_TO_MVOLTS 0.0080586
#define GFORCE_CONVERSION 0.0022

static int h48c_dio_pin;	// Bi-directional data to/from host pin
static int h48c_clk_pin;	// Synchronous clock input pin
static int h48c_cs_pin;		// Chip select input pin
static int h48c_zerog_pin;// Zero-G pin

void
h48c_open(int dio_pin, int clk_pin, int cs_pin, int zerog_pin)
{
	h48c_dio_pin = dio_pin;
	h48c_clk_pin = clk_pin;
	h48c_cs_pin = cs_pin;
	h48c_zerog_pin = zerog_pin;
	
	SET_HIGH(h48c_cs_pin); // deselect H48C
	SET_OUTPUT(h48c_cs_pin); // set CS pin as an OUTPUT
}

/**
 * h48c_gforce_of_axis - G-force of a given axis.
 * @axis: Axis.
 *
 * Return value:
 *
 * Integer.
 *
 * Description:
 *
 * To "read" g-force of a given axis we actually read the voltage output from
 * that axis and calculate g-force using this formula:
 *
 *           G = ((axis_count - vref_count) / 4095) * (3.3 / 0.3663)
 *
 * In the formula, axis_count and vref_count are expressed in counts from the 
 * ADC; 4095 is the maximum output count from a 12-bit ADC channel; 3.3 is the
 * H48C supply voltage; 0.3663 is the H48C output voltage for 1g (when operating
 * at 3.3v). In practive this can be simplified to:
 *
 *                G = (axis_count - vref_count) * 0.0022
 *
 *                                  or
 *
 *                  G = (axis_count - vref_count) / 455
 */
int
h48c_gforce_of_axis(uint32_t select)
{
	int32_t vref_count; // ref voltage adc counts
	int32_t axis_count; // axis voltage adc counts

	// Read vref and axis counts
	vref_count = h48c_read_value(H48C_SELECT_VREF);
	_waitcnt(_cnt() + 300); // 1usec
	axis_count = h48c_read_value(select);
	
	// Calculate g-force for axis
	if (axis_count >= vref_count)
		// positive g-force
		return (axis_count - vref_count);// * GFORCE_CONVERSION;
	else
		// negative g-force
		return -(vref_count - axis_count);// * GFORCE_CONVERSION;
}

/**
 * h48c_free_fall - Free-fall detection.
 *
 * Return value:
 *
 * Returns 1 if accelerometer is free-falling, or 0 otherwise.
 *
 * Description:
 *
 * From this theoretic characteristic, when the indicated values (output value) 
 * of three axes show zero simultaneously, it can be judged that this 
 * accelerometer is in the condition of free-fall. Here, the free-fall means 
 * the state where there is no external force to be added to the accelerometer 
 * except for the gravity. On the occasion that the object is thrown upward, the
 * object will be in the condition of free-fall from the moment of  leaving a 
 * hand. When air resistance is large, it acts as external force. And, when an 
 * accelerometer is equipped in the point except for the rotation center of the 
 * object (for example, sphere), is rotating and falling, the centrifugal force 
 * acts by its rotation. Then, none of these above cases can be strictly called 
 * free-fall.
 *
 * http://www.parallax.com/Portals/0/Downloads/docs/prod/acc/H48CPrinciplesofFree-FallDetection.pdf
 *
 * 
 */
int8_t
h48c_free_fall()
{
	return (!!(_ina() & PIN(h48c_zerog_pin)));
}

void
h48c_close()
{
	SET_HIGH(h48c_cs_pin); // deselect H48C
}

/**
 * h48c_read_value - Read value through an MCP3204 ADC
 */
uint32_t
h48c_read_value(uint32_t select)
{
	uint32_t value;
	
	SET_LOW(h48c_cs_pin); // make CS pin LOW (select H48C)

	stamp_shiftout(h48c_dio_pin, h48c_clk_pin, MSBFIRST, 5, select);
	value = stamp_shiftin(h48c_dio_pin, h48c_clk_pin, MSBPOST, 13);
	
	SET_HIGH(h48c_cs_pin); // make CS pin HIGH (deselect H48C)
	
	return (value & DATA_MASK); // leave only the data
}

