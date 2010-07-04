/*
 * bbos/lib/driver/bbos_device.h
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

/*** BeginHeader */
#ifndef __BBOS_DEVICE_H
#define __BBOS_DEVICE_H

/** The device identifier type */
typedef uint16_t bbos_device_id_t;

/**
 * The basic device structure. Keeps an information about single device.
 * This structure will used by driver by default.
 */
struct bbos_device {
	/* Device state */
	int8_t state;
};

typedef struct bbos_device bbos_device_t;

/**
 * Basic device states.
 */
enum {
	BBOS_DEVICE_STATE_CLOSE	= 0,
	BBOS_DEVICE_STATE_OPENE	= 1
};

#endif /* __BBOS_DEVICE_H */
/*** EndHeader */

