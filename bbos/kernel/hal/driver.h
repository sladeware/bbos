/*
 * Hardware Abstraction Layer (HAL).
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <stdio.h>
#include <bbos/kernel.h>
#include <bbos/kernel/port.h>

static bbos_thread_id_t driver_thread_id;
static bbos_port_id_t driver_listen_port_id;
static bbos_port_message_t driver_message;
#ifdef BBOS_DRIVER_DEBUG
static int8_t driver_init_complete = FALSE;
#endif

/**
 * bbos_driver_idle - Runs when the driver does not have a new message.
 */
static void bbos_driver_idle();

/**
 * bbos_driver_demultiplexer - Processes commands from the Messenger.
 */
static void bbos_driver_demultiplexer(int command, void *data);

/**
 * bbos_driver_bootstrapper - Boot initialization.
 * @id: Driver identifier in system.
 * @listen_port: The port to be listen by messenger.
 *
 * Description:
 *
 * The Bootstrapper performs all actions required to setup and initialize the 
 * device when the system is booted. It prepares the device for opening by the 
 * Driver Core. All driver tables are initialized by the Bootstrapper along with
 * allocation of IRQs and setup of any ISRs.
 */
static void 
bbos_driver_bootstrapper(bbos_thread_id_t thread_id, bbos_port_id_t listen_port_id)
{
	driver_thread_id = thread_id;
	driver_listen_port_id = listen_port_id;
#ifdef BBOS_DRIVER_DEBUG
	driver_init_complete = TRUE;
#endif
}

/**
 * bbos_driver_messenger - Read and write messages.
 *
 * Description:
 *
 * The Messenger processes message sent by outside world and also sends message
 * back.
 *
 * At the same time, the Messenger demultiplexes messages into commands/payload 
 * and passes them to the driver core. It bundles commands/payloads and sends to
 * the port requested by the driver core.
 */
static void
bbos_driver_messenger()
{
	// To improve the performance we check initialization part only in debug mode 
#ifdef BBOS_DRIVER_DEBUG
	if (!driver_init_complete) {
		return;
	}
#endif

	// When the listen port is empty the driver goes to the idle mode
  if (bbos_port_is_empty(driver_listen_port_id)) {
    bbos_driver_idle();
    return;
  }

	bbos_port_read(driver_listen_port_id, &driver_message);

	bbos_driver_demultiplexer(driver_message.id, driver_message.data);

  // Do simple return without response when we do not need to reply
  if (BBOS_PORT_IS_VALID(driver_message.feedback)) {
    return;
  }

#if defined(BBOS_ENABLE_MM) && defined(BBOS_DRIVER_USE_MM)
	bbos_free(msg);
	
	msg = (bbos_port_message_t *)bbos_alloc(sizeof(struct bbos_port_message));
#endif
  
  bbos_port_write(driver_message.feedback, &driver_message);
}

