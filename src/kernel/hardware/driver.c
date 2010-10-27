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
  int16_t command; // Command to driver
  void *private; // Data to process
};

struct bbos_driver {
  bbos_thread_id_t owner; // thread which own the driver
  int8_t *name;
  int16_t version;
  int8_t *config;
};

/* Global device driver table. Keeps information about all the drivers. */
struct bbos_driver bbos_driver_table[BBOS_NUMBER_OF_DRIVERS];

/**
 * bbos_driver_execute - Execute command.
 * @command: Command code.
 */
void
bbos_driver_execute(bbos_driver_command_t command)
{
  switch (command) {
  case BBOS_DRIVER_COMMAND(BBOS_DRIVER_OPEN):
    break;

  case BBOS_DRIVER_COMMAND(BBOS_DRIVER_CLOSE):
    break;

  default:
    bbos_driver_demultiplexer(command, data);
    break;  
  }
}

/**
 * bbos_driver_core - Processes commands from the Messenger.
 * @command: Driver command to be executed.
 * @data: Special data.
 */
void
bbos_driver_core(bbos_driver_command_t command, void *data)
{

  bbos_driver_execute(command);
}

/**
 * bbos_driver_messenger - Process driver message.
 * @driver: Pointer to the driver structure.
 *
 * Description:
 *
 * The Messenger processes message sent by other threads and also sends messages
 * to other threads. At the same time, the Messenger demultiplexes messages into
 * commands/payload and passes them to the driver core. It bundles 
 * commands/payloads and sends to the thread requested by the driver core.
 *
 * Return value:
 *
 * Messenger do not return any state code. Instead it calls bbos_driver_error() 
 * routine.
 */
void
bbos_driver_messenger(bbos_port_id_t id, struct bbos_driver_request *request, \
		      struct bbos_driver_response *response)
{
  /* Read a new message. Unless we have a message, send specified code. */
  bbos_port_read(id, request, sizeof(struct bbos_driver_request));

  /* Not an error if we do not have a message */
  if (request == NULL) {
    return;
  }

  switch (request->command) {
    default:
      err = bbos_driver_private_command();
  }

  /* Let us free the request data */
  bbos_mempool_free(request->pool, request->data);

  /* Send message back with results */
  response->err = err;
  response->sender = bbos_schedule_identify_thread();

  bbos_port_write(message->sender, response, sizeof(strurct bbos_driver_response));
}

/**
 * bbos_driver_register - Register device driver.
 * @id: Driver identifier.
 * @owner: Thread identifier which owns the driver.
 * @name: String name.
 * @version: Version number.
 * @config: Config string.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_hardware_register_driver(bbos_driver_id_t id, bbos_thread_id_t owner, \
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

/**
 * bbos_driver_unregister - Unregister device driver.
 * @id: Device driver identifier.
 *
 * Return value:
 *
 * Generic error code.
 */
bbos_return_t
bbos_driver_unregister(bbos_driver_id_t id)
{
  assert(id < BBOS_NUMBER_OF_DRIVERS);

  bbos_driver_table[id].owner = BBOS_UNKNOWN_THREAD_ID;
  bbos_driver_table[id].name = NULL;
  bbos_driver_table[id].version = 0;
  bbos_driver_table[id].config = NULL;

  return BBOS_SUCCESS;
}

#endif /* BBOS_NUMBER_OF_DRIVERS > 0 */

