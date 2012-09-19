/*
 * Platform selection logic.
 *
 * Copyright (c) 2011 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */
#ifndef __BB_CONFIG_HOST_PLATFORM_H
#define __BB_CONFIG_HOST_PLATFORM_H
/*
 * Detect which platform we are using and define BB_PLATFORM_CONFIG_H as
 * needed.
 */
#if defined(linux) || defined(__linux) || defined(__linux__)
#define BB_CONFIG_HOST_PLATFORM_H "bb/config/host_platforms/linux.h"
#endif /* linus? */

#endif /* __BB_CONFIG_HOST_PLATFORM_H */
