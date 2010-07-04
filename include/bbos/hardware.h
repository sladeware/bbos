/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_HARDWARE_H
#define __BBOS_HARDWARE_H

/** Default values */
#define BBOS_DEFAULT_HARDWARE_ARCH     generic
#define BBOS_DEFAULT_HARDWARE_CPU      generic
#define BBOS_DEFAULT_HARDWARE_PLATFORM generic

/*
 * The architecture and cpu (both of them) can be omitted unless you do
 * not know them or they are not important within current application.
 */
#ifndef BBOS_HARDWARE_ARCH
//#warning "Architecture was not specified"
#define BBOS_HARDWARE_ARCH  BBOS_DEFAULT_HARDWARE_ARCH

#ifdef BBOS_HARDWARE_CPU
#error "CPU can be specified only with architecture"
#else
#define BBOS_HARDWARE_CPU BBOS_DEFAULT_HARDWARE_CPU
#endif /* BBOS_HARDWARE_ARCH */

#else
/**
 * The BBOS_HARDWARE_ARCH macro is responsible for identifying the architecture.
 * BBOS fails unless it is defined correctly.
 */
#ifndef BBOS_HARDWARE_ARCH
#error "BBOS_HARDWARE_ARCH definition was not specified"
#endif /* BBOS_HARDWARE_ARCH */

#ifndef BBOS_HARDWARE_CPU
#error "BBOS_HARDWARE_CPU definition was not specified"
#endif /* BBOS_HARDWARE_CPU */

/**
 * The BBOS_HARDWARE_PLATFORM macro is responsible for the platform identifying.
 * BBOS fails unless it will be defined correctly.
 */
#ifndef BBOS_HARDWARE_PLATFORM
//#warning "BBOS_HARDWARE_PLATFORM definition was not specified"
#define BBOS_HARDWARE_PLATFORM  BBOS_DEFAULT_HARDWARE_PLATFORM
#endif /* BBOS_HARDWARE_PLATFORM */

#endif /* architecture and platform */

/**
 * Precondition: BBOS_HARDWARE_ARCH and BBOS_HARDWARE_CPU are defined.
 *
 * Example: BBOS_HARDWARE_ARCH=mips32 and BBOS_HARDWARE_CPU=m4k
 *  #include BBOS_HARDWARE_ARCH_INC(init.h)	includes bbos/hardware/arch/mips32/init.h
 *  #include BBOS_HARDWARE_CPU_INC(init.h)	includes bbos/hardware/arch/mips32/m4k/init.h
 *
 * Example: BBOS_HARDWARE_PLATFORM=PIC32MX795F512L
 *  #include BBOS_HARDWARE_PLATFORM_INC(init.h) includes bbos/hardware/platform/PIC32MX795F512L/init.h
 */
#define BBOS_HARDWARE_ARCH_INC(x)      <bbos/hardware/arch/BBOS_HARDWARE_ARCH/x>
#define BBOS_HARDWARE_CPU_INC(x)       <bbos/hardware/arch/BBOS_HARDWARE_ARCH/BBOS_HARDWARE_CPU/x>
#define BBOS_HARDWARE_PLATFORM_INC(x)  <bbos/hardware/BBOS_HARDWARE_PLATFORM/x>

#endif /* __BBOS_HARDWARE_H */
