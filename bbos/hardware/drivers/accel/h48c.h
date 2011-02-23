/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

/**
 * @file h48c.h
 * @brief Hitachi H48C 3 axis accelerometer driver interface
 */

#ifndef __H48C_H
#define __H48C_H

/**
 * @name ADC control bit selections
 */
// @{
/** Analog output voltage of X axis. */
#define H48C_SELECT_AOX  0x18
/** Analog output voltage of Y axis. */
#define H48C_SELECT_AOY  0x19
/** Analog output voltage of Z axis. */
#define H48C_SELECT_AOZ  0x1A
/** Select reference voltage. */
#define H48C_SELECT_VREF 0x1B
// @}

/** 13-bit data mask */
#define DATA_MASK 0x1FFF 

/**/

struct h48c_pins {
  int dio; 
  int clk;
  int cs; 
  int zerog;
};

/* Messages */

#ifndef H48C_FREE_FALL
#error "Please define H48C_FREE_FALL message"
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
void h48c();

#endif



