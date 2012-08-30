/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file vegimeter_config.h
 * @brief Common config file for vegimeter parts
 *
 * @mainpage Vegimeter
 *
 * Design Document:
 * https://docs.google.com/document/d/15U6fNcfc0FeTir46BejYtf14oOK8b4B83Xh8CfdANuI/edit

 * Architecture Document:
 * https://docs.google.com/drawings/d/1-p6k4T24JzqQ8bxHXnyh6eOs4cmtS7jffa-5HD3LI7g/edit
 *
 * @section todo TODO
 * @li Skeleton (Python Configuration)
 * @li Thermometer Driver
 * @li Controller threads
 * @li Button Driver
 * @li Heater and Pump Driver
 * @li Loading and running app on a Propeller and using all 8 cogs
 * @li Shared Memory API
 * @li Shared Memory Based Inter-Mapping Communication
 * @li Automatic identification and assignment of device GPIO pins
 *     from Fritzing Sketch
 * @li "Connect" Controller cog with other cogs, so they communcate
 *     with IMC and shared memory
 * @li System Integration and Testing
 */

#ifndef __VEGIMETER_CONFIG_H
#define __VEGIMETER_CONFIG_H

/* Define shared memory space */
#define VEGIMETER_SHMEM_START_ADDR 24576 /* 24K */
#define VEGIMETER_BUTTONS_ADDR (VEGIMETER_SHMEM_START_ADDR)

#endif /* __VEGIMETER_CONFIG_H */
