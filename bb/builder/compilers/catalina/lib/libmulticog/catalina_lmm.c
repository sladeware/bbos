/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <catalina_lmm.h>
#include <catalina_time.h>

/*
 * Include the LMM dynamic kernel formatted as a C array. The array was produced
 * using the following commands:
 *
 *       homespun Catalina_LMM_dynamic.spin -b -o catalina_lmm
 *       spinc catalina_lmm.binary > catalina_lmm_array.h
 */
#include <catalina_lmm_array.h>
#define lmm_array catalina_lmm_array /* alias */

/**
 * Load LMM kernel into selected cog to start specified C function on it.
 *
 * More about the Propeller Large Memory Model can be found here:
 *  http://propeller.wikispaces.com/Large+Memory+Model
 *
 * @function: address of C function to run (defined as 'void f(void)')
 * @stack: address of TOP of stack to use (i.e. points just after last long)
 * @cog_id: cog ID.
 *
 * @return cog used, or -1 on any error
 *
 * @seealso: _coginit().
 */
cog_id_t
lmm_init_cog(void function(void), unsigned long* stack, cog_id_t cog_id)
{
  cog_id_t cog;
  struct {
    unsigned long REG;
    unsigned long PC;
    unsigned long SP;
  } cog_data;

  cog_data.REG = _registry(); /* regisrtry address */
  cog_data.PC = (unsigned long)function; /* address of C function */
  cog_data.SP = (unsigned long)stack; /* top of stack */
  cog = _coginit((int)&cog_data >> 2, (int)lmm_array >> 2, cog_id);
  delay_ms(100); /* small delay for cog to initialize */
  return cog;
}
