/*
 * SPI Engine.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __SPI_H
#define __SPI_H

#include <bbos/kernel.h>

// Used for SHIFTIN routines
#define MSBPRE   0 
#define LSBPRE   1
#define MSBPOST	 2 // Data is msb-first; sample bits after clock pulse
#define LSBPOST  3

// Use for SHIFTOUT routines
#define LSBFIRST 4 // Least significant bit first (per-word bits-on-wire)
#define MSBFIRST 5 // Data is shifted out msb-first

/* Prototypes */

void shiftout(uint32_t dpin, uint32_t cpin, uint32_t mode, uint32_t bits, 
              uint32_t data);

uint32_t shiftin(uint32_t dpin, uint32_t cpin, uint32_t mode, uint32_t bits);

#endif

