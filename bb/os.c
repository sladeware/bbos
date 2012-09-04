/*
 * This file implements os.h interface.
 *
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
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
 */

#include <bb/os.h>
#include BBOS_PROCESSOR_FILE(sio.h)
#define bbos_printf sio_printf

#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR  \
  " (" BB_PLATFORM_NAME ")"                                         \
  " (" BB_COMPILER_NAME ")"                                         \
  "\n";
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */

void
bbos()
{
#ifndef BBOS_CONFIG_SKIP_BANNER_PRINTING
  bbos_printf("%s", bbos_banner);
#endif /* BBOS_CONFIG_SKIP_BANNER_PRINTING */
  //bbos_init();
}
