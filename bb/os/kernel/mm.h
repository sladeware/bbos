/*
 * Memory management
 *
 * Copyright (c) 2011 Sladeware LLC
 */

#include <bb/config/stdlib/stdlib.h>

#define bbos_malloc(sz) malloc(sz)
#define bbos_free(ptr) free(ptr)

