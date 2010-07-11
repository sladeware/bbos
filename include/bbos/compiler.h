/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_COMPILER_H
#define __BBOS_COMPILER_H

/* Trap pasters of __FUNCTION__ at compiler-time */
#if __GNUC__ > 2 || __GNUC_MINOR__ >= 95
#define __FUNCTION__ (__func__)
#endif

/* Catalina compiler */
#ifdef __CATALINA__
#include <bbos/compiler/catalina.h>
#endif /* __CATALINA__ */

#endif /* __BBOS_COMPILER_H */
