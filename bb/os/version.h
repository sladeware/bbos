/*
 * Please review http://en.wikipedia.org/wiki/Software_versioning .
 *
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
 */

#ifndef __BBOS_VERSION_H
#define __BBOS_VERSION_H

/* Major version number. */
#define BBOS_MAJOR_VERSION 0

/* Minor version number. */
#define BBOS_MINOR_VERSION 2

/* Patch number. */
#define BBOS_PATCH_VERSION 0

/* Tail. */
#define BBOS_VERSION_TAIL Alpha3

#define __BBOS_MAKE_VERSION_STR(a, b, c, d) #a"."#b"."#c"-"#d
#define BBOS_MAKE_VERSION_STR(a, b, c, d) __BBOS_MAKE_VERSION_STR(a, b, c, d)

/* Version string representation. */
#define BBOS_VERSION_STR                                        \
  BBOS_MAKE_VERSION_STR(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, \
                        BBOS_PATCH_VERSION, BBOS_VERSION_TAIL)

#define BBOS_MAKE_VERSION(major, minor, patch)  \
  (((major) << 16) | ((minor) << 8) | (patch))

#define BBOS_VERSION                                                    \
  BBOS_MAKE_VERSION(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, BBOS_PATCH_VERSION)

#define BBOS_CHECK_VERSION(major, minor, patch)                     \
  (bbos_version_number() >= BBOS_MAKE_VERSION(major, minor, patch))

// Obtain version number.
#define bbos_version_number()                   \
  (BBOS_VERSION)

#endif // __BBOS_VERSION_H
