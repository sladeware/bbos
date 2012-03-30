/*
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __VEGIMETER_CONFIG_H
#define __VEGIMETER_CONFIG_H

/* Common BBOS setup for all the instances */
#define BBOS_SKIP_BANNER_PRINTING
#define BBOS_CONFIG_PROCESSOR propeller_p8x32

/* Define shared memory space */
#define VEGIMETER_SHMEM_START_ADDR 24576 /* 24K */
#define VEGIMETER_BUTTONS_ADDR (VEGIMETER_SHMEM_START_ADDR)

#endif /* __VEGIMETER_CONFIG_H */
