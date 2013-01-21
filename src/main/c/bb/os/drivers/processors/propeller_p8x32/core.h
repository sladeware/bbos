/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#ifndef __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_CORE_H
#define __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_CORE_H

typedef int cog_id_t;

#ifdef __CATALINA__
#include <catalina_cog.h>

#elif defined(__GNUC__)

/**
 * Returns the id of the current cog.
 */
#define propeller_get_cog_id() cogid()

#endif

#define bbos_get_core_id() propeller_get_cog_id()

int detect_free_cogs();
char count_free_cogs();

#endif /* __BB_OS_DRIVERS_PROCESSORS_PROPELLER_P8X32_CORE_H */
