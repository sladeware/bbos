/*
 * Copyright (c) 2012 Sladeware LLC
 */

#ifndef _CATALINA_MULTICOG_SUPPORT_H
#define _CATALINA_MULTICOG_SUPPORT_H

#include <catalina_cog.h>

typedef int cog_id_t;

#define LMM_kernel_new_cog(function, stack) \
  LMM_kernel_init_cog(function, stack, ANY_COG)

cog_id_t LMM_kernel_init_cog(void function(void), unsigned long* stack,
  cog_id_t cog_id);

#define LMM_kernel_stop_cog(cog_id) \
  _cogstop(cog_id)

#endif /* _CATALINA_MULTICOG_SUPPORT_H */
