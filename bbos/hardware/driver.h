/*
 * Driver interface.
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __BBOS_DRIVER_H
#define __BBOS_DRIVER_H

struct bbos_driver_request {
	bbos_thread_id_t sender;
	int output;
	int command;
	void *data;
	size_t size;
};

struct bbos_driver_response {
	bbos_thread_id_t sender;
	int command;
	void *data;
	size_t size;
	bbos_return_t error;
};

enum bbos_driver_commands {
	BBOS_DRIVER_OPEN = 0,
	BBOS_DRIVER_CLOSE,
};

#endif /* __BBOS_DRIVER_H */

