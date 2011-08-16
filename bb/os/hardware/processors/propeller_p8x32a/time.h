/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file time.h
 */

#ifndef __P8X32A_TIME_H
#define __P8X32A_TIME_H

#include <bb/os/kernel.h>

/* 1 millisecond (1 ms) is a cycle time for frequency 1 kHz; */
PROTOTYPE(void bbos_sleep_ms, (int milliseconds));
PROTOTYPE(void bbos_sleep_sec, (int seconds));

#endif /* __P8X32A_TIME_H */
