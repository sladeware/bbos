/*
 * Large Memory Model (LMM) support.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

/*
 * LMM kernel can be loaded into another cog to
 * execute C functions concurrently with the main kernel.
 */

#ifndef _CATALINA_LMM_H
#define _CATALINA_LMM_H

#include <catalina_cog.h>

typedef int cog_id_t;

#define lmm_new_cog(function, stack)           \
  lmm_init_cog(function, stack, ANY_COG)

cog_id_t lmm_init_cog(void function(void), unsigned long* stack,
                      cog_id_t cog_id);

#define lmm_stop_cog(cog_id)                   \
  _cogstop(cog_id)

#endif /* _CATALINA_LMM_H */
