/*
 * OS config
 *
 * Copyright (c) 2011 Sladeware LLC
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
#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

#include <bb/config.h> /* MUST be first */
#include <bb/config/stdlib/stdint.h> /* MUST be second */

/* Include main OS configuration file defined by user. */
#include BB_CONFIG_OS_H /* MUST be third */

#include <bb/os/version.h>
#include <bb/os/types.h>

/* Include some standard libraries from config compatibility. */
#include <bb/config/stdlib/stdio.h>
#include <bb/config/stdlib/stddef.h>

/* Hardware macro */

/* This macro builds path for the proper driver header file. */
#define BBOS_DRIVER_FILE(file) \
  <bb/os/drivers/file>

#ifndef BBOS_CONFIG_PROCESSOR
#error Processor name has to be provided.
#endif

/* This macro builds path for the proper processor header file. Allows
   to find files related to processor in use. For example, if you are
   using the propeller_p8x32a processor and you would like to include
   time.h file, the BBOS_PROCESSOR_FILE(time.h) may produce
   "bb/os/drivers/processors/propeller_p8x32a/time.h". However this
   macro can be redefined in order to load files from different
   places. */
#ifndef BBOS_PROCESSOR_FILE
#define BBOS_PROCESSOR_FILE(file) \
  BBOS_DRIVER_FILE(processors/BBOS_CONFIG_PROCESSOR/file)
#endif /* BBOS_PROCESSOR_FILE */

/* Include BBOS_CONFIG_PROCESSOR_H header file with processor
   configurations. If BBOS_CONFIG_PROCESSOR_H macro was not defined,
   BBOS_CONFIG_PROCESSOR can be defined as a processor's name in order
   to find it in standard driver library by using selection logic. For
   a standard processors this name equals the directory name where the
   processor's configuration is located. */
#if defined(BBOS_CONFIG_PROCESSOR_H)
# include BBOS_CONFIG_PROCESSOR_H
#elif defined(BBOS_CONFIG_PROCESSOR)
# define BBOS_CONFIG_PROCESSOR_H BBOS_PROCESSOR_FILE(config.h)
#else
/*# warning Cannot define processor in use.                     \
  Please define BBOS_CONFIG_PROCESSOR_H or BBOS_CONFIG_PROCESSOR.
*/
#endif /* BBOS_CONFIG_PROCESSOR_H */
#include BBOS_CONFIG_PROCESSOR_H

/* By default BBOS_CONFIG_DEBUG macro equals to the ANSI standrad NDEBUG
   macro value. */
#ifndef BBOS_CONFIG_DEBUG
#define BBOS_CONFIG_DEBUG NDEBUG
#endif

#include <bb/os/kernel/config.h>

#endif /* __BBOS_CONFIG_H */
