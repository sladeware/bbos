/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file delay.h
 * @brief Propeller P8X32 time handling
 */

#ifndef __P8X32A_DELAY_H
#define __P8X32A_DELAY_H

#include <bb/os/config.h>

/* 1 millisecond (1 ms) is a cycle time for frequency 1 kHz; */
PROTOTYPE(void bbos_delay_ms, (int milliseconds));
PROTOTYPE(void bbos_delay_sec, (int seconds));

#endif /* __P8X32A_TIME_H */
