/*
 * Copyright (c) 2010 Slade Maurer, Alexander
 */

#include <bbos.h>

#if BBOS_NUMBER_OF_DEVICE_DRIVERS > 0

void
bbos_device_driver_register(bbos_device_driver_id_t driver_id,
bbos_thread_id_t tid, int8_t *name, int16_t version, int8_t *config,
void *private)
{
	assert(driver_id < BBOS_NUMBER_OF_DEVICE_DRIVERS);
	assert(tid < BBOS_NUMBER_OF_THREADS);

	bbos_process_device_driver_table[driver_id].tid = tid;
	bbos_process_device_driver_table[driver_id].name = name;
	bbos_process_device_driver_table[driver_id].version = version;
	bbos_process_device_driver_table[driver_id].config = config;
	bbos_process_device_driver_table[driver_id].private = private;
}

#endif /* BBOS_NUMBER_OF_DEVICE_DRIVERS > 0 */

