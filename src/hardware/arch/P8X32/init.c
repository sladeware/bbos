/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */
#include <bbos_config.h>
#include <bbos/hardware.h>

#include BBOS_HARDWARE_ARCH_INC(init.h)
#include BBOS_HARDWARE_ARCH_INC(microkernel/cpu.h)

#include BBOS_HARDWARE_PLATFORM_INC(init.h)
#include BBOS_HARDWARE_BOARD_INC(init.h)

#include <catalina_cog.h>

void
arch_init()
{
  unsigned cpu_hz;

  cpu_init();
  platform_init();
  board_init();

  cpu_hz = _clockfreq();
  printf("CPU running at %lu MHz\n", (cpu_hz / 1000) / 1000);

  // TODO: show CPU mode
}

