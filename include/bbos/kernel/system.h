/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_KERNEL_SYSTEM_H
#define __BBOS_KERNEL_SYSTEM_H

#ifdef __cplusplus
extern "C" {
#endif

extern const int8_t bbos_banner[];

/* Prototypes */

extern void bbos_init();
extern void bbos_test();
extern void bbos_start();
extern void bbos_stop();
extern void bbos_panic(const char *fmt, ...);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_KERNEL_SYSTEM_H */


