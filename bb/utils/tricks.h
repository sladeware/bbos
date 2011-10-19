/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/utils/tricks.h
 * @brief C tricks for string concatenation, etc.
 *
 * The purpose of this library is to provide basic macro-tricks, so user will be
 * able to sefely use them in other libraries. This library <b>does not</b> use 
 * any config file (such as @c bb/config.h), so it can be used even in 
 * configuration header files.
 */

#ifndef __BB_TRICKS_H
#define __BB_TRICKS_H

/**
 * This macro joins the three arguments together, even when one of the 
 * arguments is itself a macro.
 */
#define BB_JOIN3(A1, A2, A3) BB_DO_JOIN3(A1, A2, A3)
#define BB_DO_JOIN3(A1, A2, A3) __BB_DO_JOIN3(A1, A2, A3)
#define __BB_DO_JOIN3(A1, A2, A3) A1##A2##A3

#define BB_TO_STR(A1) __BB_TO_STR(A1)
#define __BB_TO_STR(A1) #A1

#endif /* __BB_TRICKS */

