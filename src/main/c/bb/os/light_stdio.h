/*
 * Copyright (c) 2012-2013 Sladeware LLC
 * Author: Oleksandr Sviridenko
 */

#ifndef __BB_OS_LIGHT_IO_H
#define __BB_OS_LIGHT_IO_H

#include "bb/config.h"
#include BBOS_PROCESSOR_FILE(sio.h)

#ifndef bb_printf
#define bb_printf printf
#endif

#ifndef bb_vprintf
#define bb_vprintf vprintf
#endif

#endif /* __BB_OS_LIGHT_IO_H */
