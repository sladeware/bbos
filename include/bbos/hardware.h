/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_HARDWARE_H
#define __BBOS_HARDWARE_H

/** Default values */
#define BBOS_DEFAULT_HARDWARE_ARCH generic

/*
 * The architecture can be omitted unless you do not know it or it's not
 * important within current application.
 */
#ifndef BBOS_HARDWARE_ARCH
//#warning "Architecture was not specified"
#define BBOS_HARDWARE_ARCH  BBOS_DEFAULT_HARDWARE_ARCH
#endif /* BBOS_HARDWARE_ARCH */

/**
 * Example: BBOS_HARDWARE_ARCH=P8X32
 *  #include BBOS_HARDWARE_ARCH_INC(init.h)	includes bbos/hardware/arch/P8X32/init.h
 *
 * Example: BBOS_HARDWARE_PLATFORM=PIC32MX795F512L
 *  #include BBOS_HARDWARE_PLATFORM_INC(init.h) includes bbos/hardware/platform/PIC32MX795F512L/init.h
 */
#define BBOS_HARDWARE_ARCH_INC(x)      <bbos/hardware/arch/BBOS_HARDWARE_ARCH/x>
#define BBOS_HARDWARE_PLATFORM_INC(x)  <bbos/hardware/platform/BBOS_HARDWARE_PLATFORM/x>
#define BBOS_HARDWARE_BOARD_INC(x)     <bbos/hardware/board/BBOS_HARDWARE_BOARD/x>

#endif /* __BBOS_HARDWARE_H */
