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

struct bbos_driver_message {
  bbos_driver_id_t id;
  int16_t command;
  void *private;
};

struct bbos_driver {
  bbos_thread_id_t owner;
  int8_t *name;
  int16_t version;
  int8_t *config;
};

struct bbos_driver bbos_driver_table[BBOS_NUMBER_OF_DRIVERS];

bbos_return_t
bbos_driver_messenger(bbos_thread_id_t *sender, bbos_driver_command_t *command, 
void **data)
{
  struct bbos_driver_message *message;

  message = (struct bbos_driver_message *)bbos_itc_receive();

  if (message == NULL) {
    return BBOS_FAILURE;
  }

  *sender = message->sender;
  *command = message->command;
  *data = message->private;

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_driver_register(bbos_driver_id_t id, bbos_thread_id_t owner, \
		     int8_t *name, int16_t version, int8_t *config)
{
  assert(id < BBOS_NUMBER_OF_DRIVERS);
  assert(owner < BBOS_NUMBER_OF_THREADS);

  bbos_driver_table[id].owner = owner;
  bbos_driver_table[id].name = name;
  bbos_driver_table[id].version = version;
  bbos_driver_table[id].config = config;

  return BBOS_SUCCESS;
}

bbos_return_t
bbos_driver_unregister(bbos_driver_id_t id)
{
  assert(id < BBOS_NUMBER_OF_DRIVERS);

  bbos_driver_table[id].owner = 0;
  bbos_driver_table[id].name = NULL;
  bbos_driver_table[id].version = 0;
  bbos_driver_table[id].config = NULL;

  return BBOS_SUCCESS;
}

#endif /* BBOS_NUMBER_OF_DRIVERS > 0 */

