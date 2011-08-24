/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/stdint.h
 * @brief A portable stdint.h header file

   <table>
   <tr>
   <th><b>Type</b></th><th><b>Description</b></th>
   </tr>
   <tr><td colspan="2" align="center"><b>8-bit types</b></td></tr>
   <tr>
   <td>@c int8_t</td>
   <td>Signed integers with values ranging from -128 to 127.</td>
   </tr>
   <tr>
   <td>@c uint8_t</td>
   <td>Unsigned integers with values ranging from 0 to 255.</td>
   </tr>
   <tr><td colspan="2" align="center"><b>16-bit types</b></td></tr>
   <tr>
   <td>@c int16_t</td>
   <td>Signed integers with values ranging from -32,768 to 32,767.</td>
   </tr>
   <tr>
   <td>@c uint16_t</td>
   <td>Unsigned integers with values ranging from 0 to 65,535.</td>
   </tr>
   <tr><td colspan="2" align="center"><b>32-bit types</b></td></tr>
   <tr>
   <td>@c int32_t</td>
   <td>Signed integers with values ranging from −2,147,483,648 to
   2,147,483,647.</td>
   </tr>
   <tr>
   <td>@c uint32_t</td>
   <td>Unsigned integers with values ranging from 0 to 4,294,967,295.</td>
   </tr>
   <tr><td colspan="2" align="center"><b>64-bit types</b></td></tr>
   <tr>
   <td>@c int64_t</td>
   <td>Signed integers with values ranging from -9,223,372,036,854,775,808 to
   9,223,372,036,854,775,807.</td>
   </tr>
   <tr>
   <td>@c uint64_t</td>
   <td>Unsigned integers with values ranging from 0 to
   18,446,744,073,709,551,615.</td>
   </tr>
   </table>
 */

#ifndef __BB_STDINT_H
#define __BB_STDINT_H

#include <bb/config.h>

#if defined(BB_HAS_STDINT_H)

#  include <stdint.h>

#else /* defined(BB_HAS_STDINT_H) */

#include <limits.h>

/* 8-bit types ************************************/

#  if UCHAR_MAX == 0xFF
     typedef char int8_t;
     typedef unsigned char uint8_t;
#  else
#    error "Defaults not correct; please hand modify bb/stdint.h"
#  endif

/* 16-bit types ***********************************/

#  if USHRT_MAX == 0xFFFF
     typedef short int16_t;
     typedef unsigned short uint16_t;
#  else
#    error "Defaults not correct; please hand modify bb/stdint.h"
#  endif

/* 32-bit types ***********************************/

#  if ULONG_MAX == 0xFFFFFFFF
     typedef long int32_t;
     typedef unsigned long uint32_t;
#  elif UINT_MAX == 0xFFFFFFFF
     typedef signed int int32_t;
     typedef unsigned int uint32_t;
#  else
#    error "Defaults not correct; please hand modify bb/stdint.h"
#  endif

/* 64-bit types ***********************************/

#  if defined(BB_HAS_LONG_LONG)

     typedef long long uint64_t;

#  else
#    error "Defaults not correct; please hand modify bb/stdint.h"
#  endif /* defined(BB_HAS_LONG_LONG) */

/**
 * Boolena type with values @c TRUE and @c FALSE.
 */
typedef unsigned char bool_t;

#endif /* defined(BB_HAS_STDINT_H) */

#endif /* __BB_STDINT_H */
