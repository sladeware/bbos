/*
 * Copyright (c) 2012 Sladeware LLC
 */
#include <bb/os.h>

#ifndef BBOS_SKIP_BANNER_PRINTING
/* Banner */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_PLATFORM_NAME ")"                                         \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif /* BBOS_SKIP_BANNER_PRINTING */

/**
 * BBOS entry point. It works in several ways. The user may define
 * bbos_main() function to describe application functionally. In this
 * case the system will automatically initialize itself and start the
 * kernel. Otherwise user will have to start kernel manually by
 * calling bbos_kernel_start().
 */
void
bbos()
{
#ifndef BBOS_SKIP_BANNER_PRINTING
  bbos_printf("%s", bbos_banner);
#endif /* BBOS_SKIP_BANNER_PRINTING */
  bbos_kernel_init();
#ifdef bbos_main
  bbos_main();
  bbos_kernel_start();
#endif
}
