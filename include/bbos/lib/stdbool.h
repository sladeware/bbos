/*
 * Portable stdbool.h for BBOS.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_LIB_PORTABLE_STDBOOL_H
#define __BBOS_LIB_PORTABLE_STDBOOL_H

/*
 * The type `bool' must promote to `int' or `unsigned int'. The constants
 * `true' and `false' must have the value 0 and 1 respectively.
 */
typedef enum {
  false = 0,
  true = 1
} bool;

/*
 * The names `true' and `false' must also be made available as macros.
 */
#define false false
#define true true

/*
 * Signal that all the definitions are present.
 */
#define __bbol_true_false_are_defined 1

#endif /* __BBOS_LIB_PORTABLE_STDBOOL_H */

