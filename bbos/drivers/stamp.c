/*
 * Stamp.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
 
#include <bbos/drivers/stamp.h>
#include <bbos/kernel/math/bitops.h>

#define PIN(pin) (1<<pin)
#define SET_HIGH(pin) _outa(PIN(pin), PIN(pin))
#define SET_LOW(pin) _outa(PIN(pin), 0)
#define SET_INPUT(pin) _dira(PIN(pin), 0)
#define SET_OUTPUT(pin) _dira(PIN(pin), PIN(pin))

static void
post_clock_pulse(uint32_t cpin)
{
	_waitcnt(_cnt() + 600);
	SET_HIGH(cpin); // set CLK pin HIGH
	_waitcnt(_cnt() + 600);
	SET_LOW(cpin); // set CLK pin LOW
}

static void
pre_clock_pulse(uint32_t cpin)
{

	SET_HIGH(cpin); // set CLK pin HIGH
	_waitcnt(_cnt() + 600);
	SET_LOW(cpin); // set CLK pin LOW
 	_waitcnt(_cnt() + 600);
}

/**
 * stamp_shiftout - Shift data out to a synchronous serial device.
 * @dpin: I/O pin that connectes to the synchronous serial device's data input.
 *        This pin will be set to output mode.
 * @cpin: --
 * @mode: The order in which data bits are to be arranged.
 * @bits: How many bits are to be output.
 *
 * Description:
 *
 * The SHIFTOUT instruction first causes the clock pin to output low and the
 * data pin to switch to output mode. Then, SHIFTOUT sets the data pin to the 
 * next bit state to be output and generates a clock pulse. SHIFTOUT continues 
 * to generate clock pulses and places the next data bit on the data pin for as 
 * many data bits as are required for transmission.
 */
void
stamp_shiftout(uint32_t dpin, uint32_t cpin, uint32_t mode, uint32_t bits, 
         uint32_t data)
{
	SET_LOW(dpin); // pre-set data pin LOW
	SET_OUTPUT(dpin); // set data pin as an OUTPUT
	
	SET_LOW(cpin); // pre-set clock pin LOW
	SET_OUTPUT(cpin); // set clock pin as an OUTPUT

	// Send data MSBFIRST
	if (mode == MSBFIRST) {
		data <<= (32 - bits);
	
		while (bits-- != 0) {
			data = rol32(data, 1);
			if (data & 1) SET_HIGH(dpin);
			else SET_LOW(dpin);
			//_outa(dpin, (data & 1) ? dpin : 0); // set data pin as HIGH or LOW
			post_clock_pulse(cpin); // generate clock puls
		}

		SET_LOW(dpin); // force data pin LOW
	}
}

/**
 * stamp_shiftin - Shift data in from a synchronous serial device.
 * @dpin: I/O pin that connectes to the synchronous serial device's data input.
 *        This pin will be set to output mode.
 * @cpin: --
 * @mode: The order in which data bits are to be arranged.
 * @bits: How many bits are to be output.
 *
 * Return value:
 *
 * Shifted in data.
 *
 * Description:
 *
 * The SHIFTIN instruction first causes the clock pin to output low and the data
 * pin to switch to input mode. Then, SHIFTIN either reads the data pin and 
 * generates a clock pulse (PRE mode) or generates a clock pulse then reads the 
 * data pin (POST mode). SHIFTIN continues to generate clock pulses and read the
 * data pin for as many data bits as are required.
 */
uint32_t
stamp_shiftin(uint32_t dpin, uint32_t cpin, uint32_t mode, uint32_t bits)
{
	uint32_t data;

	SET_INPUT(dpin); // set data pin as an INPUT

	SET_LOW(cpin); // pre-set clock pin LOW
	SET_OUTPUT(cpin); // set clock pin as an OUTPUT

	data = 0; // clear output

	if (mode == MSBPOST) {
		while (bits-- != 0) {
			pre_clock_pulse(cpin);
			data = (data << 1) | !!(_ina() & PIN(dpin));
		}
	}
	
	return data;
}


