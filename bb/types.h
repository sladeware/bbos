/*
 * Copyright (c) 2011 Sladeware LLC
 */

/**
 * @file bb/types.h
 * @brief Important platform data type definitions
 *
 * It is considered good programming practice to use these definitions, instead
 * of the underlying base type. By convention, all type names have postfix
 * @b _t.
 */

#ifndef __BB_TYPES_H
#define __BB_TYPES_H

#ifndef _SIZE_T
#define _SIZE_T
/**
 * The type @c size_t holds all results of the sizeof operator. At first glance,
 * it seems obvious that it should be an unsigned int, but this is not always
 * the case.
 */
typedef unsigned int size_t;
#endif

#ifndef _SSIZE_T
#define _SSIZE_T
/**
 * The type @c ssize_t is the signed version of @c size_t.
 */
typedef int ssize_t;
#endif


#endif /* __BB_TYPES_H */
