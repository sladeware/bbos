/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

/**
 * @file h48c.c
 * @brief Hitachi H48C 3 axis accelerometer driver
 *
 * The Hitachi H48C Tri-Axis Accelerometer is an integrated module that can 
 * sense gravitational (g) force of ±3g on three axes (X, Y, and Z). The module 
 * contains an onboard regulator to provide 3.3-volt power to the H48C, analog 
 * signal conditioning, and an MCP3204 (four channel, 12-bit) analog-to-digital 
 * onverter to read the H48C voltage outputs. Acquiring measurements from the 
 * module is simplified through a synchronous serial interface. 
 */
 
/*
 *        +---------+
 * CLK ---| 1 o   6 |--- Vdd (+5V)
 * DIO ---| 2     5 |--- CS
 * Vss ---| 3     4 |--- Zero-G
 *        +---------+
 *
 * Pin definitions:
 *
 * CLK    : Synchronous clock input.
 * DIO    : Bi-directional data to/from host.
 * Vss    : Power supply ground
 * Zero-G : "Free-fall" output; active-high
 * CSS    : Chip select input; active-low
 * Vdd    : +5V
 */

#include <stdio.h>
#include <bbos/kernel/system.h>
#include <bbos/kernel/error_codes.h>
#include <bbos/hardware/drivers/spi/spi_stamp.h>	
#include <bbos/hardware/drivers/accel/h48c.h>
#include <catalina_cog.h>
#include <catalina_hmi.h>

#define PIN(p) (1<<p)
#define SET_HIGH(p) _outa(PIN(p), PIN(p))
#define SET_LOW(p) _outa(PIN(p), 0)
#define SET_OUTPUT(p) _dira(PIN(p), PIN(p))

/** Counts to millivolts. */
#define COUNTS_TO_MVOLTS 0.0080586
/** G-force conversion. */
#define GFORCE_CONVERSION 0.0022

/** @name Pins */
// @{
/** Bi-directional data to/from host pin. */
static int h48c_dio_pin;	
/** Synchronous clock input pin. */
static int h48c_clk_pin;	
/** Chip select input pin. */
static int h48c_cs_pin;
/** Zero-G pin. */
static int h48c_zerog_pin;
// @}


static void
h48c_open(int dio_pin, int clk_pin, int cs_pin, int zerog_pin)
{
  h48c_dio_pin = dio_pin;
  h48c_clk_pin = clk_pin;
  h48c_cs_pin = cs_pin;
  h48c_zerog_pin = zerog_pin;
	
  SET_HIGH(h48c_cs_pin); // deselect H48C
  SET_OUTPUT(h48c_cs_pin); // set CS pin as an OUTPUT
}

static void
h48c_close()
{
  SET_HIGH(h48c_cs_pin); // deselect H48C
}

/**
 * G-force of a given axis.
 *
 * To "read" g-force of a given axis we actually read the voltage output from
 * that axis and calculate g-force using this formula:
 *
 * G = ((axis_count - vref_count) / 4095) * (3.3 / 0.3663)
 *
 * In the formula, axis_count and vref_count are expressed in counts from the 
 * ADC; 4095 is the maximum output count from a 12-bit ADC channel; 3.3 is the
 * H48C supply voltage; 0.3663 is the H48C output voltage for 1g (when operating
 * at 3.3v). In practive this can be simplified to:
 *
 * G = (axis_count - vref_count) * 0.0022
 *
 * or
 *
 * G = (axis_count - vref_count) / 455
 *
 * @param axis Axis.
 *
 * @return
 *
 * Integer.
 */
static int
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
 * Free-fall detection.
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
 * @return
 *
 * Returns 1 if accelerometer is free-falling, or 0 otherwise.
 */
static int8_t
h48c_free_fall()
{
  return (!!(_ina() & PIN(h48c_zerog_pin)));
}

/**
 * Read value through an MCP3204 ADC.
 */
static uint32_t
h48c_read_value(uint32_t select)
{
  uint32_t value;
	
  SET_LOW(h48c_cs_pin); // make CS pin LOW (select H48C)

  stamp_shiftout(h48c_dio_pin, h48c_clk_pin, MSBFIRST, 5, select);
  value = stamp_shiftin(h48c_dio_pin, h48c_clk_pin, MSBPOST, 13);
	
  SET_HIGH(h48c_cs_pin); // make CS pin HIGH (deselect H48C)
	
  return (value & DATA_MASK); // leave only the data
}

/** 
 * H48C accelerometer driver thread.
 */
void
h48c()
{
  static struct bbos_message message;
  struct h48c_pins *pins;

  // Start waiting for a message
  if (bbos_port_receive(H48C, &message) != BBOS_SUCCESS)
    {
      return;
    }

  switch (message.id)
    {
    case BBOS_DRIVER_INIT:
      break;
    case BBOS_DRIVER_OPEN:
      pins = (struct h48c_pins *)message.data;
      h48c_open(pins->dio, pins->clk, pins->cs, pins->zerog);
      break;
    case BBOS_DRIVER_CLOSE:
      h48c_close();
      break;
    case H48C_GFORCE_AOX:
      break;
    case H48C_FREE_FALL:
      *(int *)message.data = h48c_free_fall();
      break;
    default:
      bbos_panic("h48c received illegal message %d", message.id);
      break;
    }

  // Do we need to send a response?
  //if (message.sender) {
  bbos_port_send(FREEFALL, &message, H48C);
  //}
}


