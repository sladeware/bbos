/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __COG_H
#define __COG_H

typedef int cog_id_t;

#ifdef __CATALINA__
#include <catalina_cog.h>

#endif /* __CATALINA__ */

int detect_free_cogs();
char count_free_cogs();

#endif /* __COGUTIL_H */
