/*
 * Copyright (c) 2011 Sladeware LLC
 */

#ifndef __BBOS_CONFIG_H
#define __BBOS_CONFIG_H

/**
 * @file bb/os/config.h
 * @brief BBOS configuration file

 @par BBOS User Settable Options

 There are some configuration-options that represent user choices. This options
 ar listed in header file defined with help of @c BBOS_H macro, that can be
 redefined in @c bb.h header file. By default it equals to @c <bbos.h> if
 the macro is not defined.

 <table>
  <tr>
   <td valign="top" align="center"><b>Macro</b></td>
   <td valign="top" align="center"><b>Description</b></td>
  </tr>
  <tr>
   <td>@c BBOS_DEBUG</td>
   <td>Define whether we need to use debug mode. By default equals to
   @c NDEBUG macro.</td>
  </tr>
  <tr>
   <td>@c BBOS_NR_THREADS</td>
   <td>Define number of threads available in this process.</td>
  </tr>
  <tr>
    <td>@c BBOS_SCHED_CONFIG_H</td>
    <td>Points to the name of the scheduler configuration file to use. Difining
    this cuts out the scheduler selection logic, and eliminates the dependency
    on the header containing that logic. For example if you are using
    @c staticscheduler scheduler, then you could define @c BB_SCHED_CONFIG_H
    to @c <bb/os/schedulers/staticscheduler.h>. By default will be used
    @c staticscheduler.</td>
  </tr>
  <tr>
    <td>@c BBOS_PROCESSOR_CONFIG_H</td>
    <td>Points to the name of the processor configuration file to use.
    For example if you are using @c Propeller @c P8X32 processor, then you could
    define @c BBOS_PROCESSOR_CONFIG_H to
    @c <bb/os/hardware/processors/propeller_p8x32/config.h>.</td>
  </tr>
  <tr>
   <td>@c BBOS_PROCESSOR_NAME</td>
   <td>If @c BBOS_PROCESSOR_CONFIG_H macro was not defined, this macro can be
   defined as a processors name in order to find it in standard hardware
   library by using selection logic. For a standard processors this name equals
   to directory name where processors configuration is located.</td>
  </tr>
 </table>

 @par BBOS Information Macros

 The following macros describe bbos features.

 <table>
  <tr>
   <th valign="top" align="center"><b>Macro</b></th>
   <th valign="top" align="center"><b>Header</b></th>
   <th valign="top" align="center"><b>Description</b></th>
  </tr>
  <tr>
   <td>@c BBOS_VERSION_STR</td>
   <td>@c <bb/os/version.h> </td>
   <td>Describes the bbos version number in MAJOR.MINOR.PATCH-TAIL format.</td>
  </tr>
  <tr>
   <td>@c BBOS_VERSION</td>
   <td>@c <bb/os/version.h> </td>
   <td>Describes the bbos version number.</td>
  </tr>
  <tr>
   <td>@c BBOS_SCHED_ENABLED</td>
   <td>@c <bb/os/kernel/sched.h></td>
   <td>Defined if scheduler was selected. If @c BBOS_SCHED_ENABLED is not
   defined the @c bbos_switch_thread() has
   to be provided in @c BBOS_H file.</td>
  </tr>
  <tr>
   <td>@c BBOS_SCHED_STR</td>
   <td>@c <bb/os/kernel/sched.h></td>
   <td>Describes the scheduler name as a string. This will be printed in
   debug mode.</td>
  </tr>
 </table>

*/

/**
 * @defgroup bbos_config Config
 * @ingroup bbos_config
 */

#include <bb/config.h> /* MUST be first */
#include <bb/stdint.h>
#include <bbos.h> /* MUST be third */

#include <bb/os/version.h>
#include <bb/os/types.h>

/**
 * @def BBOS_DEBUG
 * @brief The BBOS debug macro equals to the ANSI standard @c NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#ifndef BBOS_DEBUG
#define BBOS_DEBUG NDEBUG
#endif

#ifndef BBOS_NR_THREADS
#error "Please define BBOS_NR_THREADS in <bbos.h>"
#endif

/**
 * @name Hardware
 * @{
 */

#ifndef BBOS_PROCESSOR_NAME
#error "BBOS_PROCESSOR_NAME was not defined"
#endif

/**
 * @def BBOS_PROCESSOR_FILE(filename)
 * @brief Build path for the proper processor header file.
 */
#ifndef BBOS_PROCESSOR_FILE
#define BBOS_PROCESSOR_FILE(filename)                   \
  <bb/os/hardware/processors/BBOS_PROCESSOR/filename>
#endif

/** @} */

/**
 * Banner.
 */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR \
  " (" BB_COMPILER_STR ")" "\n";

#endif /* __BBOS_CONFIG_H */
