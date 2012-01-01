/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <catalina_multicog_support.h>

/*
 * Include the dynamic kernel formatted as a C array. The array was produced
 * using the following commands:
 *
 *       homespun Catalina_LMM_dynamic.spin -b -o LMM
 *       spinc LMM.binary > LMM_array.h
 */
#include "LMM_array.h"

/**
 * Start a C function in a new available cog.
 *
 * @func: address of C function to run (defined as 'void f(void)')
 * @stack: address of TOP of stack to use (i.e. points just after last long)
 * @cog_id: cog ID.
 *
 * @return cog used, or -1 on any error
 */
cog_id_t
LMM_kernel_init_cog(void function(void), unsigned long* stack, cog_id_t cog_id)
{
   cog_id_t cog;
   struct {
      unsigned long REG;
      unsigned long PC;
      unsigned long SP;
   } cog_data;

   cog_data.REG = _registry(); /* regisrtry address */
   cog_data.PC  = (unsigned long)function; /* address of C function */
   cog_data.SP  = (unsigned long)stack; /* top of stack */
   cog = _coginit((int)&cog_data >> 2, (int)LMM_array >> 2, cog_id);
   wait(100); /* small delay for cog to initialize */
   return cog;
}

