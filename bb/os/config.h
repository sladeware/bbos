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
 are listed in header file defined with help of @c BB_CONFIG_OS_H macro, that 
 can be redefined in @c bb.h header file. By default it equals to @c <bbos.h> if
 the macro is not defined. Please not that @c BBOS_CONFIG_ prefix is reserved 
 for configuration macros. They are listed in the following table:

 <table>
  <tr>
   <th valign="top" align="center">Macro</th>
   <th valign="top" align="center">Description</th>
  </tr>
  <tr>
   <td>@c BBOS_CONFIG_DEBUG</td>
   <td>Define whether we need to use debug mode. By default @c BBOS_DEBUG equals 
   to @c NDEBUG macro.</td>
  </tr>
  <tr><td colspan="2"><b>Kernel</b></td></tr>
  <tr>
   <td>@c BBOS_CONFIG_NR_THREADS</td>
   <td>Define number of threads available in this process.</td>
  </tr>
  <tr>
    <td>@c BBOS_CONFIG_SCHED_H</td>
    <td>Points to the name of the scheduler configuration file to use. Difining
    this cuts out the scheduler selection logic, and eliminates the dependency
    on the header containing that logic. For example if you are using
    @c staticscheduler scheduler, then you could define @c BB_CONFIG_SCHED_H
    to @c \"bb/os/kernel/schedulers/staticscheduler.h\". By default will be used
    @c staticscheduler.</td>
  </tr>
  <tr><td colspan="2"><b>Processor</b></td></tr>
  <tr>
    <td>@c BBOS_CONFIG_PROCESSOR_H</td>
    <td>Points to the name of the processor configuration file to use.
    For example if you are using @c Propeller @c P8X32 processor, then you could
    define @c BBOS_CONFIG_PROCESSOR_H to
    @c \"bb/os/hardware/processors/propeller_p8x32/config.h\".</td>
  </tr>
  <tr>
   <td>@c BBOS_CONFIG_PROCESSOR_NAME</td>
   <td>If @c BBOS_CONFIG_PROCESSOR_H macro was not defined, this macro can be
   defined as a processors name in order to find it in standard hardware
   library by using selection logic. For a standard processors this name equals
   to directory name where processors configuration is located.</td>
  </tr>
  <tr>
   <td>@c BBOS_CONFIG_PROCESSOR_GPIO</td>
   <td>If defined, the processors GPIO driver will be configured and scheduled.
   It will be available as @c BBOS_PROCESSOR_GPIO_DRIVER_NAME and scheduled with
   @c BBOS_PROCESSOR_GPIO_DRIVER_ID id.</td>
  </tr>
 </table>

 @par BBOS Information Macros

 The following macros describe bbos features.

 <table>
  <tr>
   <th valign="top" align="center"><b>Macro</b></th>
   <th valign="top" align="center"><b>Description</b></th>
  </tr>
  <tr>
   <td>@c BBOS_VERSION_STR</td>
   <td>Describes the bbos version number in MAJOR.MINOR.PATCH-TAIL format.</td>
  </tr>
  <tr>
   <td>@c BBOS_VERSION</td>
   <td>Describes the bbos version number.</td>
  </tr>
 </table>
 
 @par BBOS Kernel Information Macros
 
 <table>
  <tr>
   <th valign="top" align="center"><b>Macro</b></th>
   <th valign="top" align="center"><b>Description</b></th>
  </tr>
  <tr>
   <td>@c BBOS_NR_THREADS</td>
   <td>Number of threads within current process.</td>
  </tr>
  <tr>
   <td>@c BBOS_SCHED_STR</td>
   <td>Describes the scheduler name as a string. This will be printed in
   debug mode.</td>
  </tr>
 </table>

 @par BBOS Hardware Information Macros

 <table>
  <tr>
   <th valign="top" align="center"><b>Macro</b></th>
   <th valign="top" align="center"><b>Description</b></th>
  </tr>
  <tr>
   <td>@c BBOS_PROCESSOR_NAME</td>
   <td></td>
  </tr>
  <tr>
   <td>@c BBOS_PROCESSOR_STR</td>
   <td>Defined as a string describing the name and number of cores, etc. of the
   processor in use.</td>
  </tr>
  <tr>
   <td>@c BBOS_PROCESSOR_FILE</td>
   <td>Allows to find files related to processor in use. For example, if the 
   using processor is @c propeller_p8x32a and you would like to include
   @c delay.h file, the <code>BBOS_PROCESSOR_FILE(delay.h)</code> will produce
   @c "bb/os/hardware/processors/propeller_p8x32a/delay.h".</td>
  </tr>
 </table>

*/

/**
 * @defgroup bbos_config Config
 * @ingroup bbos_config
 */


#include <bb/config.h> /* MUST be first */
#include <bb/stdint.h> /* MUST be second */

/* Include main OS configuration file with application configurations defined
   by user */
#ifndef BB_CONFIG_OS_H
# error "BB_CONFIG_OS_H was not defined"
#endif
#include BB_CONFIG_OS_H /* MUST be third */

#include <bb/os/version.h>
#include <bb/os/types.h>

#include <bb/utils/tricks.h> /* Use some tricks for string concat, etc. */

#ifndef BBOS_CONFIG_DEBUG
# define BBOS_CONFIG_DEBUG NDEBUG
#endif
/**
 * @def BBOS_DEBUG
 * @brief The BBOS debug macro equals to the ANSI standard @c NDEBUG macro.
 * Learn more http://www.embedded.com/story/OEG20010311S0021
 */
#define BBOS_DEBUG BBOS_CONFIG_DEBUG

/**
 * @name Hardware
 * @{
 */

#if defined(BBOS_CONFIG_PROCESSOR_H)
# include BBOS_CONFIG_PROCESSOR_H
#elif defined(BBOS_CONFIG_PROCESSOR_NAME)
# define BBOS_CONFIG_PROCESSOR_H \
    <bb/os/hardware/processors/BBOS_CONFIG_PROCESSOR_NAME/config.h>
#else
# error "Can not define processor in use. Please define " \
  "BBOS_CONFIG_PROCESSOR_H or BBOS_CONFIG_PROCESSOR_NAME"
#endif /* defined(BBOS_CONFIG_PROCESSOR_H) */
#include BBOS_CONFIG_PROCESSOR_H

/**
 * @def BBOS_PROCESSOR_FILE(filename)
 * @brief Build path for the proper processor header file.
 */
#ifndef BBOS_PROCESSOR_FILE
#define BBOS_PROCESSOR_FILE(filename)                   \
  <bb/os/hardware/processors/BBOS_PROCESSOR_NAME/filename>
#endif

/** @} */

/**
 * Banner.
 */
const static char bbos_banner[] = "BBOS version " BBOS_VERSION_STR \
  " (" BBOS_ME "@" BB_PLATFORM_STR ")" \
  " (" BB_COMPILER_STR ")" "\n";

#endif /* __BBOS_CONFIG_H */
