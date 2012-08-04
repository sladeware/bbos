/*
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Author: Oleksandr Sviridenko
 */

#include <bb/os.h>

#ifndef BBOS_SKIP_BANNER_PRINTING
// Banner
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_PLATFORM_NAME ")"                                         \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif // BBOS_SKIP_BANNER_PRINTING

// BBOS entry point. The user may define bbos_main() function to describe
// application functionally between kerenl initialization and running.
// NOTE: the system will automatically initialize itself and start the kernel.
void
bbos()
{
#ifndef BBOS_SKIP_BANNER_PRINTING
  bbos_printf("%s", bbos_banner);
#endif // BBOS_SKIP_BANNER_PRINTING
  bbos_kernel_init();
#ifdef bbos_main
  bbos_main();
#endif
  bbos_kernel_start();
}
