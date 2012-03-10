/*
 * Copyright (c) 2012 Sladeware LLC
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

#ifdef __GNUC__
/* Include DIRA, OUTA, etc. */
#  include <propeller.h>
#endif

/* Common Propeller primitives */

/** Wait until system counter reaches a value. */
#undef propeller_waitcnt
/** Return lock to pool */
#undef propeller_lockret

#ifdef __CATALINA__
#  define propeller_get_clockfreq() _clockfreq()
#  define propeller_get_cnt() _cnt()
#  define propeller_waitcnt(a) _waitcnt(a)
#  define propeller_locknew(lock) _locknew(lock)
#  define propeller_lockclr(lock) _lockclr(lock)
#  define propeller_lockset(lock) _lockset(lock)
#  define propeller_lockret(lock) _lockret(lock)
#elif __GNUC__
#  define propeller_get_clockfreq() CLKFREQ
#  define propeller_get_cnt() CNT
#  define propeller_waitcnt(a) waitcnt(a)
#  define propeller_locknew(lock) locknew(lock)
#  define propeller_lockclr(lock) lockclr(lock)
#  define propeller_lockset(lock) lockset(lock)
#  define propeller_lockret(lock) lockret(lock)
#endif

#endif /* __PROPELLER_P8X32_CONFIG_H */
