/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __H48C_ACCEL_H
#define __H48C_ACCEL_H

/**
 * @file bb/os/drivers/accel/h48c/core.h
 * @brief Hitachi H48C 3 axis accelerometer driver interface
 *
 * The Hitachi H48C Tri-Axis Accelerometer is an integrated module that can
 * sense gravitational (g) force of ±3g on three axes (X, Y, and Z). The module
 * contains an onboard regulator to provide 3.3-volt power to the H48C, analog
 * signal conditioning, and an MCP3204 (four channel, 12-bit) analog-to-digital
 * onverter to read the H48C voltage outputs. Acquiring measurements from the
 * module is simplified through a synchronous serial interface.
 *
 * @image html http://www.parallax.com/Portals/0/Images/Prod/2/280/28026-M.jpg
 *
 @verbatim
         +---------+
  CLK ---| 1 o   6 |--- Vdd (+5V)
  DIO ---| 2     5 |--- CS
  Vss ---| 3     4 |--- Zero-G
         +---------+
 @endverbatim
 *
 * Pin definitions:
 *
 * @par
 * @b CLK: Synchronous clock input\n
 * @par
 * @b DIO: Bi-directional data to/from host\n
 * @par
 * @b Vss: Power supply ground\n
 * @par
 * @b Zero-G: "Free-fall" output; active-high\n
 * @par
 * @b CSS: Chip select input; active-low\n
 * @par
 * @b Vdd: +5V\n
 */


/**
 * @name ADC control bit selections
 */
// @{
/**
 * @def H48C_SELECT_AOX
 * @brief Analog output voltage of X axis.
 */
#define H48C_SELECT_AOX  0x18
/**
 * @def H48C_SELECT_AOY
 * @brief Analog output voltage of Y axis.
 */
#define H48C_SELECT_AOY  0x19
/**
 * @def H48C_SELECT_AOZ
 * @brief Analog output voltage of Z axis.
 */
#define H48C_SELECT_AOZ  0x1A
/**
 * @def H48C_SELECT_VREF
 * @brief Select reference voltage.
 */
#define H48C_SELECT_VREF 0x1B
// @}

/**
 * @def DATA_MASK
 * @brief 13-bit data mask
 */
#define DATA_MASK 0x1FFF

/**
 * @struct h48c_pins
 * @brief Pin definitions
 */
struct h48c_pins {
  int16_t dio; /**< Bi-directional data to/from host */
  int16_t clk; /**< Synchronous clock input */
  int16_t cs; /**< Chip select input */
  int16_t zerog; /**< "Free-fall" output */
};

/* Messages */

#ifndef H48C_FREEFALL
#error "Please define H48C_FREEFALL message"
#endif
#ifndef H48C_GFORCE_AOX
#error "Please define H48C_GFORCE_AOX message"
#endif
#ifndef H48C_GFORCE_AOY
#error "Please define H48C_GFORCE_AOY message"
#endif
#ifndef H48C_GFORCE_AOZ
#error "Please define H48C_GFORCE_AOZ message"
#endif

/* Prototypes */
void h48c_runner();

#endif /* __H48C_ACCEL_H */
