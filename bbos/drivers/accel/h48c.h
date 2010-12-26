/*
 * H48C Accelerometer
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __H48C_H
#define __H48C_H

#include <bbos/drivers/stamp.h>

/*
 * ADC control bit selections:
 *
 * +----- Start bit
 * |+---- Single/Differential bit
 * ||+--- D2*
 * |||+-- D1
 * ||||+- D0
 * |||||
 * 11000 - Analog output voltage of X axis
 * 11001 - Analog output voltage of Y axis
 * 11010 - Analog output voltage of Z axis
 * 11011 - Reference voltage
 *
 * D2*, D1, D0 - bits are used to select the input channel configuration.
 * D2* - reserved bit.
 */
 
#define H48C_SELECT_AOX  0x18
#define H48C_SELECT_AOY  0x19
#define H48C_SELECT_AOZ  0x1A
#define H48C_SELECT_VREF 0x1B

#define DATA_MASK 0x1FFF // 13-bit data mask

#endif



