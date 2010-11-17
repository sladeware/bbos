/*
 * CAN (Controller Area Network) driver on Microchip PIC32MX family 
 * microcontrollers.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

/*
 * Check the compiler version. We need Microchip C32 v1.06 or higher.
 */
#if __C32_VERSION__ < 106
#error "PIC32MX_CAN requires version C32 >= 1.06(" __C32_VERSION ")" 
#endif

/*
 * Include the library with already existed low-level abstraction of the CAN 
 * module on Microchip PIC32MX family microcontrollers.
 */
#include <peripheral/CAN.H>

void
pic32mx_can_init()
{
}

