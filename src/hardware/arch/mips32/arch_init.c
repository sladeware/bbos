/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/hardware/arch/mips32/arch_init.h>

void
arch_init()
{
  /*
   * Configure the device for maximum performance, but do not change the PBDIV clock divisor.
   * Given the options, this function will change the program Flash wait states,
   * RAM wait state and enable prefetch cache, but will not change the PBDIV.
   * The PBDIV value is already set via the pragma FPBDIV option above.
   */
  SYSTEMConfig(SYS_FREQ, SYS_CFG_WAIT_STATES | SYS_CFG_PCACHE);
}
