/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file version.h
 * @brief Version control
 *
 * Please review http://en.wikipedia.org/wiki/Software_versioning .
 */

#ifndef __BBOS_VERSION_H
#define __BBOS_VERSION_H

/**
 * @def BBOS_MAJOR_VERSION
 * @brief Major version number.
 */
#define BBOS_MAJOR_VERSION 0

/**
 * @def BBOS_MINOR_VERSION
 * @brief Minor version number.
 */
#define BBOS_MINOR_VERSION 2

/**
 * @def BBOS_PATCH_VERSION
 * @brief Patch number.
 */
#define BBOS_PATCH_VERSION 0

/**
 * @def BBOS_VERSION_TAIL
 * @brief Tail.
 */
#define BBOS_VERSION_TAIL Alpha3

#define __BBOS_MAKE_VERSION_STR(a, b, c, d) #a"."#b"."#c"-"#d
#define BBOS_MAKE_VERSION_STR(a, b, c, d) __BBOS_MAKE_VERSION_STR(a, b, c, d)

/**
 * @def BBOS_VERSION_STR
 * @brief Version string representation.
 */
#define BBOS_VERSION_STR                                        \
  BBOS_MAKE_VERSION_STR(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, \
                        BBOS_PATCH_VERSION, BBOS_VERSION_TAIL)

#define BBOS_MAKE_VERSION(major, minor, patch)  \
  (((major) << 16) | ((minor) << 8) | (patch))

#define BBOS_VERSION                                                    \
  BBOS_MAKE_VERSION(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, BBOS_PATCH_VERSION)

#define BBOS_CHECK_VERSION(major, minor, patch)                     \
  (bbos_version_number() >= BBOS_MAKE_VERSION(major, minor, patch))

/**
 * @def bbos_version_number
 * @brief Obtain version number.
 */
#define bbos_version_number()                   \
  (BBOS_VERSION)

#endif /* __BBOS_KERNEL_H */
