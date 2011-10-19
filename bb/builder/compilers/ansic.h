/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file ansic.h
 * @brief Whether the compiler has enough conformance to Standard C for BB
 *
 * This header file attempts to decide whether the compiler has enough
 * conformance to Standard C to take advantage of.
 *
 * Read more: http://en.wikipedia.org/wiki/ANSI_C
 */

#ifndef __ANSIC_H
#define __ANSIC_H

/* Try to define automatically whether ANSI C Standard is supported */
#ifndef BB_COMPILER_ANSIC_COMPLIANT
#if __STDC == 1
#define BB_COMPILER_ANSIC_COMPLIANT 31459 /* compiler claims full ANSI conformance */
#elif __GNUC__
#define BB_COMPILER_ANSIC_COMPLIANT 31459
#endif
#endif /* BB_COMPILER_ANSIC_COMPLIANT */

#ifdef BB_COMPILER_ANSIC_COMPLIANT /* keep everything for ANSI prototypes */
#define PROTOTYPE(function, params) function params
#define ARGS(params) params

#define VOIDSTAR void*
#define VOID void
#define CONST const
#define VOLATILE volatile
#define SIZET size_t

#else /* throw away the parameters for K&R prototypes */

#define PROTOTYPE(function, params) function()
#define ARGS(params) ()

#define VOIDSTAR void*
#define VOID void
#define CONST
#define VOLATILE
#define SIZET int

#endif /* BB_COMPILER_ANSIC_COMPLIANT */

#endif /* __ANSIC_H */
