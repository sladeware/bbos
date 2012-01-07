/*
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __BB_ASSERT_H
#define __BB_ASSERT_H

#undef BB_ASSERT

#include <assert.h>
#define BB_ASSERT(expr) assert(expr)

#endif /* __BB_ASSERT_H */
