/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __COG_H
#define __COG_H

#ifdef __CATALINA__
#include <catalina_cog.h>

#define coginit(par, code, id)                  \
  _coginit(par, code, id)

#define cognew(par, code)                       \
  coginit(par, code, ANY_COG)

#define cogid() _cogid()

#endif /* __CATALINA__ */

int detect_free_cogs();
char count_free_cogs();

#endif /* __COGUTIL_H */
