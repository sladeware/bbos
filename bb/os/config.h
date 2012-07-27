// Bionic Bunny OS config
//
// Copyright (c) 2011-2012 Sladeware LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//       http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Author: Oleksandr Sviridenko

#ifndef __BB_OS_CONFIG_H
#define __BB_OS_CONFIG_H

// Include main platform config, MUST be first.
#include <bb/config.h>

// Include main OS configuration file defined by user.
#include BB_CONFIG_OS_H // MUST be second

#include <bb/os/version.h>
#include <bb/os/types.h>

// Include some standard libraries from config compatibility.
#include <bb/config/stdlib/stdio.h>
#include <bb/config/stdlib/stddef.h>

// Hardware macro

// This macro builds path for the proper driver header file.
#define BBOS_DRIVER_FILE(file) \
  <bb/os/drivers/file>

#ifndef BBOS_CONFIG_PROCESSOR
#  error Processor name has to be provided.
#endif

// This macro builds path for the proper processor header file. Allows to find
// files related to processor in use. For example, if you are using the
// propeller_p8x32a processor and you would like to include time.h file, the
// BBOS_PROCESSOR_FILE(time.h) may produce
// "bb/os/drivers/processors/propeller_p8x32a/time.h". However this macro can be
// redefined in order to load files from different places.
#ifndef BBOS_PROCESSOR_FILE
#define BBOS_PROCESSOR_FILE(file) \
  BBOS_DRIVER_FILE(processors/BBOS_CONFIG_PROCESSOR/file)
#endif // BBOS_PROCESSOR_FILE

// Include BBOS_CONFIG_PROCESSOR_H header file with processor configurations. If
// BBOS_CONFIG_PROCESSOR_H macro was not defined, BBOS_CONFIG_PROCESSOR can be
// defined as a processor's name in order to find it in standard driver library
// by using selection logic. For a standard processors this name equals the
// directory name where the processor's configuration is located.
#if defined(BBOS_CONFIG_PROCESSOR_H)
# include BBOS_CONFIG_PROCESSOR_H
#elif defined(BBOS_CONFIG_PROCESSOR)
# define BBOS_CONFIG_PROCESSOR_H BBOS_PROCESSOR_FILE(config.h)
#else
/*# warning Cannot define processor in use.                     \
  Please define BBOS_CONFIG_PROCESSOR_H or BBOS_CONFIG_PROCESSOR.
*/
#endif // BBOS_CONFIG_PROCESSOR_H
#include BBOS_CONFIG_PROCESSOR_H

// By default BBOS_CONFIG_DEBUG macro equals to the ANSI standrad NDEBUG macro
// value.
#ifndef BBOS_CONFIG_DEBUG
#define BBOS_CONFIG_DEBUG NDEBUG
#endif

// Check number of threads.
#ifndef BBOS_CONFIG_NR_THREADS
# error Please define BBOS_CONFIG_NR_THREADS in BB_CONFIG_OS_H
#endif
#if BBOS_CONFIG_NR_THREADS < 1
# error System requires atleast one thread
#endif // BBOS_CONFIG_NR_THREADS

// System threads
#define BBOS_NR_SYSTEM_THREADS 0

// Set final number of threads
#define BBOS_NR_THREADS (BBOS_CONFIG_NR_THREADS + BBOS_NR_SYSTEM_THREADS)

// By default the number of ports in zero. In this case port interface wont be
// supported.
#ifndef BBOS_CONFIG_NR_PORTS
# define BBOS_CONFIG_NR_PORTS 0
#endif
#define BBOS_NR_PORTS BBOS_CONFIG_NR_PORTS

// Scheduler selection logic. If scheduler wasn't selected, FCFS scheduler
// will be taken.
//#ifndef BBOS_COFNIG_SCHED_H
//# include <bb/os/kernel/config/scheduler.h>
//#endif
//#include BBOS_CONFIG_SCHED_H

#endif // __BB_OS_CONFIG_H
