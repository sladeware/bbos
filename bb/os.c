#include <bb/os.h>

/* Banner */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_PLATFORM_NAME ")"                                         \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";

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
  printf("%s", bbos_banner);
  bbos_kernel_init();
#ifdef bbos_main
  bbos_main();
  bbos_kernel_start();
#endif
}
