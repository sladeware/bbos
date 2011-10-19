/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/os/driver.h
 * @brief Driver interface
 */

#ifndef __BBOS_DRIVER_H
#define __BBOS_DRIVER_H

/**
 * @def BBOS_DRIVER_API(name, method, args)
 * @brief Get an access to the driver's API
 */
#define BBOS_DRIVER_API(name, method, args)     \
  name ## method ## args

/**
 * @def BBOS_DRIVER_PROTO(ret, name, method, args)
 * @brief Get driver's prototype
 */
#define BBOS_DRIVER_PROTO(ret, name, method, args)  \
  ret BBOS_DRIVER_API(name, method, args)

#endif /* __BBOS_DRIVER_H */
