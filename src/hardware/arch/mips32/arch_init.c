/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/hardware/arch/mips32/arch_init.h>

// Configuration Bits
#ifndef OVERRIDE_CONFIG_BITS
#pragma config FNOSC    = PRIPLL        // Oscillator Selection
#pragma config FPLLIDIV = DIV_2         // PLL Input Divider (PIC32 Starter Kit: use divide by 2 only)
#pragma config FPLLMUL  = MUL_20        // PLL Multiplier
#pragma config FPLLODIV = DIV_1         // PLL Output Divider
#pragma config FPBDIV   = DIV_1         // Peripheral Clock divisor
#pragma config FWDTEN   = OFF           // Watchdog Timer
#pragma config WDTPS    = PS1           // Watchdog Timer Postscale
#pragma config FCKSM    = CSDCMD        // Clock Switching & Fail Safe Clock Monitor
#pragma config OSCIOFNC = OFF           // CLKO Enable
#pragma config POSCMOD  = XT            // Primary Oscillator
#pragma config IESO     = OFF           // Internal/External Switch-over
#pragma config FSOSCEN  = OFF           // Secondary Oscillator Enable
#pragma config CP       = OFF           // Code Protect
#pragma config BWP      = OFF           // Boot Flash Write Protect
#pragma config PWP      = OFF           // Program Flash Write Protect
#pragma config ICESEL   = ICS_PGx2      // ICE/ICD Comm Channel Select
#pragma config DEBUG    = OFF           // Debugger Disabled for Starter Kit
#endif // OVERRIDE_CONFIG_BITS

#define SYS_FREQ		(80000000)

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
