/*
 * Copyright (c) 2012 Sladeware LLC
 */
#ifndef __SIO_H
#define __SIO_H

void sio_put_char(char c);
void sio_put_string(char* s);
void sio_put_hex(unsigned n);
void sio_printf(const char* format, ...);

/* By default SIO_LOCK_PRINTING is enabled */
#define SIO_LOCK_PRINTING

#ifdef SIO_COGSAFE_PRINTING
/*
 * Note, once SIO_COGSAFE_PRINTING was enabled, SIO_LOCK_PRINTING will
 * be also automatically enabled.
 */
#define SIO_LOCK_PRINTING
void sio_cogsafe_printf(const char* format, ...);
#endif

#ifdef SIO_LOCK_PRINTING
void sio_lock_printf(int lock, const char* format, ...);
#endif

#endif
