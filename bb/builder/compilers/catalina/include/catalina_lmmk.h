/*
 * Large Memory Model Kernel (LMMK) support.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

/*
 * LMM kernel can be loaded into another cog to
 * execute C functions concurrently with the main kernel.
 */

#ifndef _CATALINA_MULTICOG_SUPPORT_H
#define _CATALINA_MULTICOG_SUPPORT_H

#include <catalina_cog.h>

typedef int cog_id_t;

#define LMMK_new_cog(function, stack)           \
  LMMK_init_cog(function, stack, ANY_COG)

cog_id_t LMMK_init_cog(void function(void), unsigned long* stack,
                       cog_id_t cog_id);

#define LMMK_stop_cog(cog_id)                   \
  _cogstop(cog_id)

#endif /* _CATALINA_MULTICOG_SUPPORT_H */
