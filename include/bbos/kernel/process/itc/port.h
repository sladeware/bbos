/*
 * The communication port interface.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_PORT_H
#define __BBOS_PORT_H

#ifdef __cplusplus
extern "C" {
#endif

/* Some well known port id's. */
#define BBOS_NIL_PORT_ID 0xFF

/*
 * If the number of ports was not defined, it equals 0.
 */
#ifndef BBOS_NUMBER_OF_PORTS
#define BBOS_NUMBER_OF_PORTS 0
#endif /* BBOS_NUMBER_OF_PORTS */

/*
 * The number of ports can be equal zero, but can not be great
 * than BBOS_MAX_NUMBER_OF_PORTS.
 */
#if BBOS_NUMBER_OF_PORTS > 0
extern bbos_port_t bbos_port_table[BBOS_NUMBER_OF_PORTS];
#endif /* BBOS_NUMBER_OF_PORTS */
#if BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS
#error "BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS"
#endif /* BBOS_NUMBER_OF_PORTS > BBOS_MAX_NUMBER_OF_PORTS */

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_PORT_H */
