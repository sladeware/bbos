/*
 * bbos/lib/driver/bbos_driver.h
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

/*** BeginHeader */
#ifndef __BBOS_DRIVER_H
#define __BBOS_DRIVER_H

#include <bbos/lib/driver/bbos_device.h>

/**
 * Basic shared driver commands.
 */
enum {
	BBOS_DRIVER_CMD_OPEN	=	0x0001,
	BBOS_DRIVER_CMD_CLOSE	=	0x0002,
	BBOS_DRIVER_CMD_READ	=	0x0003,
	BBOS_DRIVER_CMD_WRITE	=	0x0004
};

/**
 * The driver message structure.
 */
typedef struct bbos_driver_msg {
	/* Device identifier */
	bbos_device_id_t device_id;

	/* Command */
	uint16_t cmd;

	/* Pointer to the buffer */
	int8_t *buf;

	/* Offset */
	uint16_t offset;

	/* Number of bytes */
	uint16_t nbytes;
} bbos_driver_msg_t;

/**
 * Builds driver structure. Each driver must define its own driver object to
 * identify it.
 */
#define BBOS_DRIVER(name, nports, ndevices) \
	struct {	\
		bbos_port_t port_table[nports];	\
		bbos_device_t device_table[ndevices];	\
	} name;

#endif // __BBOS_DRIVER_H
/*** EndHeader */


