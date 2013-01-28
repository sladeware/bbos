/*
 * Catalina compiler support
 *
 * Copyright (c) 2011 Sladeware LLC
 */

/*
 * Catalina is ANSI C compliant (C89 with some C99 features) and so defines
 * COMPILER_ANSIC_COMPLIANT macro. See manual for more details.
 */

#define BB_COMPILER_ANSIC_COMPLIANT
#include <bb/config/compilers/ansic.h>

#define BB_HAS_STDINT_H
#define BB_HAS_LONG_LONG

#define BB_COMPILER_NAME "Catalina"
