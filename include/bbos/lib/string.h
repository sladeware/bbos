/*
 * string.h header file plus some extra string routines.
 *
 * Copyrigth (c) 2010 Slade Marurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_STRING_H
#define __BBOS_LIB_STRING_H

#include <bbos/compiler.h>
#include <bbos/lib/stdint.h>
#include <string.h>

extern size_t strlen(const char *s);
extern size_t strnlen(const char *s, size_t count);

extern int xtoa(const char* src, char* dest);

#endif /* __BBOS_LIB_STRING_H */

