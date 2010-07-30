/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

#define BBOS_HARDWARE_ARCH P8X32
#define BBOS_HARDWARE_PLATFORM P8X32A-Q44
#define BBOS_HARDWARE_BOARD propeller_demo_board

#define BBOS_NUMBER_OF_CONFIG_THREADS 8
#define BBOS_NUMBER_OF_PORTS 1

#define LED16_ID 0
#define LED17_ID 1
#define LED18_ID 2
#define LED19_ID 3
#define LED20_ID 4
#define LED21_ID 5
#define LED22_ID 6
#define LED23_ID 7

#define bbos_thread_switch led_switcher

#endif /* __BBOS_CONFIG_H */
