/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __COG_H
#define __COG_H

typedef int cog_id_t;

#ifdef __CATALINA__
#include <catalina_cog.h>

#define coginit(par, code, id) _coginit(par, code, id)
#define cognew(par, code) coginit(par, code, ANY_COG)
#define cogid() _cogid()
#define cogstop(cog_id) _cogstop(cog_id)

#endif /* __CATALINA__ */

int detect_free_cogs();
char count_free_cogs();

#endif /* __COGUTIL_H */
