/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_SYSTEM_H
#define __BBOS_SYSTEM_H

#ifdef __cplusplus
extern "C" {
#endif

extern const int8_t bbos_banner[];

/* Enumerate values used for system states */
extern enum bbos_system_states {
  BBOS_SYSTEM_INITIALIZATION,
  BBOS_SYSTEM_TESTING,
  BBOS_SYSTEM_RUNNING
} bbos_system_state;

/* Prototypes */

extern bbos_return_t bbos();
extern void bbos_init();
extern void bbos_test();
extern void bbos_start();
extern void bbos_stop();
extern void bbos_panic(const char *fmt, ...);

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_SYSTEM_H */


