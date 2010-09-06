/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_DEVICE_DRIVER_H
#define __BBOS_DEVICE_DRIVER_H

#ifdef __cplusplus
extern "C" {
#endif

#if BBOS_NUMBER_OF_DEVICE_DRIVERS > 0

typedef int16_t bbos_device_driver_id_t;

struct bbos_device_driver_vec {
	bbos_thread_id_t tid;
	int8_t *name;
	int16_t version;
	int8_t *config;
	void *private;
};

typedef int8_t bbos_device_driver_state_t;

struct bbos_device_driver {
	bbos_device_driver_state_t state_table[BBOS_NUMBER_OF_DEVICE_DRIVERS];
};

void bbos_device_driver_register(bbos_device_driver_id_t driver_id, \
	bbos_thread_id_t tid, int8_t *name, int16_t version, int8_t *config, \
	void *private);

void bbos_device_driver_unregister(bbos_device_driver_id_t driver_id);

#endif /* BBOS_NUMBER_OF_DEVICE_DRIVERS > 0 */

#ifdef __cplusplus
}
#endif

#endif /* __BBOS_DEVICE_DRIVER_H */

