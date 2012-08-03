/*
 * Copyright (c) 2012 Sladeware LLC
 * Author: Oleksandr Sviridenko
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __PROPELLER_P8X32_CONFIG_H
#define __PROPELLER_P8X32_CONFIG_H

#if defined(__GNUC__) /* defined(__PROPELLER__) &&  */
/*
 * We use the hubtext attribute to make sure functions
 * go into hub memory even with xmm code.
 *
 * This is a GCC super-power. Put code in HUB RAM.
 * Sometimes code in XMM programs is time sensitive.
 * Use HUBTEXT before a function declaration to make
 * sure code is run from HUB instead of external memory.
 * Performance of code run from external memory is
 * unpredictable across platforms.
 */
#define HUBTEXT_SEC __attribute__((section(".hubtext")))
/*
 * Use these defines to tell compiler linker to put
 * data and code (.text) into HUB RAM.
 * This is mostly useful in XMM and XMMC modes
 * where data must be shared in hub or
 * where code must execute as fast as possible
 */
#define HUBDATA_SEC __attribute__((section(".hub")))

/* For variables that should go in cog memory */
#define COGMEM __attribute__((cogmem))
/* For functions that use cog "call/ret" calling (nonrecursive) */
#define NATIVE __attribute__((native))
/* For functions with no epilogue or prologue: these should never
   return */
#define NAKED __attribute__((naked))

/* Load 16 registers local to a cog: PAR, CNT, INA, INB, OUTA, OUTB,
   DIRA, DIRB, CTRA, CTRB, FRQA, FRQB, PHSA, PHSB, VCFG, VSCL. */
#include <propeller.h>
#else
#define HUBCODE
#endif

/* Common Propeller primitives */

/* Wait until system counter reaches a value. */
#undef propeller_waitcnt
/* Return lock to pool */
#undef propeller_lockret

#ifdef __CATALINA__
#define propeller_cogid() _cogid()
#define propeller_get_clockfreq() _clockfreq()
#define propeller_get_cnt() _cnt()
#define propeller_waitcnt(a) _waitcnt(a)
#define propeller_locknew(lock) _locknew(lock)
#define propeller_lockclr(lock) _lockclr(lock)
#define propeller_lockset(lock) _lockset(lock)
#define propeller_lockret(lock) _lockret(lock)

#elif __GNUC__
#define propeller_cogid() cogid()
#define propeller_get_clockfreq() CLKFREQ
#define propeller_get_cnt() CNT
#define propeller_waitcnt(a) waitcnt(a)
#define propeller_locknew(lock) locknew(lock)
#define propeller_lockclr(lock) lockclr(lock)
#define propeller_lockset(lock) lockset(lock)
#define propeller_lockret(lock) lockret(lock)
#endif

#endif /* __PROPELLER_P8X32_CONFIG_H */
