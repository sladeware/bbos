/*
 * Copyright (c) 2010 Slade Maurer, Alexander
 */

#include <bbos.h>

#if BBOS_NUMBER_OF_DEVICES > 0

struct bbos_device_vec bbos_device_table[BBOS_NUMBER_OF_DEVICES];

bbos_return_t
bbos_device_init(struct bbos_device *dev, bbos_device_id_t id)
{
  bbos_device_id_t i;

  assert(id < BBOS_NUMBER_OF_DEVICES);

  dev->id = id;

  for(i=0; i<BBOS_NUMBER_OF_DEVICES; i++) {
    dev->state_table[i] = 0;
  }

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_device_register(struct bbos_device *dev,
		     bbos_thread_id_t tid, int8_t *name, int16_t version, 
		     int8_t *config, void *private)
{
  assert(dev->id < BBOS_NUMBER_OF_DEVICES);
  assert(tid < BBOS_NUMBER_OF_THREADS);

  bbos_device_table[dev->id].tid = tid;
  bbos_device_table[dev->id].name = name;
  bbos_device_table[dev->id].version = version;
  bbos_device_table[dev->id].config = config;
  bbos_device_table[dev->id].private = private;

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_device_unregister(struct bbos_device *dev)
{
  assert(dev->id < BBOS_NUMBER_OF_DEVICES);
  assert(tid < BBOS_NUMBER_OF_THREADS);

  bbos_device_table[dev->id].tid = 0;
  bbos_device_table[dev->id].name = NULL;
  bbos_device_table[dev->id].version = 0;
  bbos_device_table[dev->id].config = NULL;
  bbos_device_table[dev->id].private = NULL;

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_device_destroy(struct bbos_device *dev)
{
  bbos_device_unregister(dev);

  return BBOS_SUCCESS;
}

#endif /* BBOS_NUMBER_OF_DEVICES > 0 */

