/*
 * Driver Hardware Abstraction Layer (HAL).
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_DRIVER_HAL_H
#define __BBOS_DRIVER_HAL_H
 
#include <bbos/hardware/driver.h>

static bbos_thread_id_t bbos_driver_id;

/* Keeps an information about current driver. */
static bbos_port_id_t bbos_driver_input;

/* Keeps message-request for the current driver, received by messenger. */
static struct bbos_driver_request bbos_driver_request;

/* 
 * Keeps message-response for the current driver, that should be formed and sent
 * by messenger.
 */
static struct bbos_driver_response bbos_driver_response;

static bbos_return_t bbos_driver_error;

/* Initialize driver structure */
#define bbos_driver_init(id, input) \
	do {\
		bbos_driver_id = id; \
		bbos_driver_input = input;\
	}\
	while(0)

/* Interface */

static bbos_return_t bbos_driver_command();

//static void bbos_driver_error();

/**
 * bbos_driver_messenger - Messenger.
 */
static void
bbos_driver_messenger()
{
	if (bbos_port_empty(bbos_driver_input)) {
		return;
	}

	bbos_port_read(bbos_driver_input, &bbos_driver_request, sizeof(bbos_driver_request));

	if ((bbos_driver_error = bbos_driver_command()) != BBOS_SUCCESS) {
		//bbos_driver_error();
	}

	bbos_driver_response.sender = bbos_driver_id;
	bbos_driver_response.command = bbos_driver_request.command;
	bbos_driver_response.data = bbos_driver_request.data;
	bbos_driver_response.size = bbos_driver_request.size;
	bbos_driver_response.error = bbos_driver_error;

	bbos_port_write(bbos_driver_request.output, &bbos_driver_response, \
		sizeof(bbos_driver_response));
}
 
#endif /* __BBOS_DRIVER_HAL_H */

