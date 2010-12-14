/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/kernel.h>
#include <bbos/kernel/port.h>

#if BBOS_NUMBER_OF_PORTS > 0

struct bbos_port port_table[BBOS_NUMBER_OF_PORTS];

/**
 * bbos_port_init - Initialize port.
 */
bbos_return_t
bbos_port_init(bbos_port_id_t id)
{
	port_table[id].first_message = NULL;
	port_table[id].last_message = NULL;

#ifdef BBOS_DEBUG
	port_table[id].init_complete = TRUE;
#endif

	return BBOS_SUCCESS;
}

bool_t
__bbos_port_is_empty(bbos_port_id_t id)
{
	return (port_table[id].first_message == NULL) ? 1 : 0;
}

/**
 * bbos_port_write - Write the record to the port.
 *
 * Description:
 *
 * Basic primitive for writing.
 */
bbos_return_t
__bbos_port_write(bbos_port_id_t id, bbos_port_message_t *msg)
{
#ifdef BBOS_DEBUG
	if (!port_table[id].init_complete) {
		return BBOS_FAILURE;
	}
#endif

	if (port_table[id].last_message == NULL) {
		port_table[id].first_message = msg;
		port_table[id].last_message = msg;
		msg->next = NULL;
		return BBOS_SUCCESS;
	}

	msg->next = port_table[id].last_message->next;
	port_table[id].last_message->next = msg;
	
	return BBOS_SUCCESS;
}

/**
 * bbos_port_read - Read the record from the port.
 *
 * Description:
 *
 * Basic primitive for reading.
 */
bbos_return_t
__bbos_port_read(bbos_port_id_t id, bbos_port_message_t *message)
{
#ifdef BBOS_DEBUG
	if (!port_table[id].init_complete) {
		return BBOS_FAILURE;
	}
#endif

	if (bbos_port_is_empty(id)) {
		return BBOS_FAILURE;
	}

	*message = *port_table[id].first_message;

	if (port_table[id].first_message == port_table[id].last_message) {
		port_table[id].last_message = NULL;
	} else {
		port_table[id].first_message = port_table[id].first_message->next;
	}

	return BBOS_SUCCESS;
}

#endif

