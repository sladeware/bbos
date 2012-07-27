/*
 * C tricks for string concatination, etc.
 *
 * Copyright (c) 2011 Sladeware LLC
 */

/* The purpose of this library is to provide basic macro-tricks, so user will be
   able to safely use them in other libraries. This library does not use any
   config file, so it can be used even in configuration header files. */

#ifndef __BB_TRICKS_H
#define __BB_TRICKS_H

/* This sequence of macros joins two arguments together, even when one of the
   arguments is itself a macro. */
#define BB_JOIN2(A1, A2) BB_DO_JOIN2(A1, A2)
#define BB_DO_JOIN2(A1, A2) __BB_DO_JOIN2(A1, A2)
#define __BB_DO_JOIN2(A1, A2) A1##A2

/* This sequence of macros joins three arguments together, even when one of the
   arguments is itself a macro. */
#define BB_JOIN3(A1, A2, A3) BB_DO_JOIN3(A1, A2, A3)
#define BB_DO_JOIN3(A1, A2, A3) __BB_DO_JOIN3(A1, A2, A3)
#define __BB_DO_JOIN3(A1, A2, A3) A1##A2##A3

#endif /* __BB_TRICKS_H */
