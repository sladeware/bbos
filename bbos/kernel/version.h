/*
 * Please review http://en.wikipedia.org/wiki/Software_versioning.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_KERNEL_VERSION_H
#define __BBOS_KERNEL_VERSION_H

#define BBOS_MAJOR_VERSION 0
#define BBOS_MINOR_VERSION 1
#define BBOS_PATCH_VERSION 8

#define BBOS_VERSION_TAIL Alpha1

#define __BBOS_MAKE_VERSION_STR(a, b, c, d) #a"."#b"."#c"-"#d
#define BBOS_MAKE_VERSION_STR(a, b, c, d) __BBOS_MAKE_VERSION_STR(a, b, c, d)

#define BBOS_VERSION_STR						\
  BBOS_MAKE_VERSION_STR(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, BBOS_PATCH_VERSION, \
			BBOS_VERSION_TAIL)

#define BBOS_MAKE_VERSION(major, minor, patch)	\
  (((major) << 16) | ((minor) << 8) | (patch))

#define BBOS_VERSION							\
  BBOS_MAKE_VERSION(BBOS_MAJOR_VERSION, BBOS_MINOR_VERSION, BBOS_PATCH_VERSION)

#define BBOS_CHECK_VERSION(major, minor, patch) \
  (bbos_version_number() >= BBOS_MAKE_VERSION(major, minor, patch))

#define bbos_version_number()\
  (BBOS_VERSION)

#endif /* __BBOS_KERNEL_VERSION_H */
