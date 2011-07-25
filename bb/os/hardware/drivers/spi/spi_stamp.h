/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __STAMP_H
#define __STAMP_H

/**
 * @file spi_stamp.h
 * @brief Stamp library
 */

/** @name SHIFTIN routines */
//@{
#define MSBPRE   0 
#define LSBPRE   1
/** Data is msb-first; sample bits after clock pulse. */
#define MSBPOST	 2
#define LSBPOST  3
//@}

/** @name SHIFTOUT routines */
//@{
/** Least significant bit first (per-word bits-on-wire). */
#define LSBFIRST 4 
/** Data is shifted out msb-first. */
#define MSBFIRST 5 
//@}

/* Prototypes */

void stamp_shiftout(uint32_t dpin, uint32_t cpin, uint32_t mode, uint32_t bits, 
         uint32_t data);
uint32_t stamp_shiftin(uint32_t dpin, uint32_t cpin, uint32_t mode, 
				uint32_t bits);

#endif

