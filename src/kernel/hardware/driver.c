/*
 * Copyright (c) 2010 Slade Maurer, Alexander
 */

#include <bbos.h>

#if BBOS_NUMBER_OF_DRIVERS > 0

enum bbos_driver_states {
  BBOS_DRIVER_IS_UNDEFINED,
  BBOS_DRIVER_IS_OPENED,
  BBOS_DRIVER_IS_CLOSED
};

struct bbos_driver_local {
  bbos_driver_state_t state;
};

struct bbos_driver_global {
  bbos_thread_id_t tid;
  int8_t *name;
  int16_t version;
  int8_t *config;
};

struct bbos_driver_global bbos_driver_global_table[BBOS_NUMBER_OF_DRIVERS];

bbos_return_t
bbos_driver_init()
{
}

bbos_return_t
bbos_driver_register(bbos_driver_id_t id, bbos_thread_id_t tid, \
		     int8_t *name, int16_t version, int8_t *config)
{
  assert(id < BBOS_NUMBER_OF_DRIVERS);
  assert(tid < BBOS_NUMBER_OF_THREADS);

  bbos_driver_global_table[id].tid = tid;
  bbos_driver_global_table[id].name = name;
  bbos_driver_global_table[id].version = version;
  bbos_driver_global_table[id].config = config;

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_driver_unregister(bbos_driver_id_t id)
{
  assert(dev->id < BBOS_NUMBER_OF_DRIVERS);
  assert(tid < BBOS_NUMBER_OF_THREADS);

  bbos_driver_global_table[id].tid = 0;
  bbos_driver_global_table[id].name = NULL;
  bbos_driver_global_table[id].version = 0;
  bbos_driver_global_table[id].config = NULL;

  return BBOS_SUCCESS;
}

#endif /* BBOS_NUMBER_OF_DRIVERS > 0 */

