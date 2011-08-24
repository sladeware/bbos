/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __BB_CONST_H
#define __BB_CONST_H

/**
 * @file bb/const.h
 * @brief Basic constants
 */

/**
 * @def FALSE
 * @brief Integer contant 0. Used for turning integers into booleans.
 */
#define FALSE 0

/**
 * @def TRUE
 * @brief Integer constant @c !FALSE or 1. Used for turning integers into
 * booleans.
 */
#define TRUE (!FALSE)

/**
 * Used in @b .h files.
 */
#define EXTERN extern

/**
 * @code PRIVATE x @endcode limits the scope of @c x.
 */
#define PRIVATE static

/**
 * @c PUBLIC is opposite to @c PRIVATE.
 */
#define PUBLIC

/**
 * Some compilers require this to be 'static'.
 */
#define FORWARD static

#endif /* __BB_CONST_H */
