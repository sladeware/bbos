/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */
 
#ifndef __BBOS_PORT_H
#define __BBOS_PORT_H

#include <string.h>
#include <bbos/kernel.h>

#define BBOS_NULL_PORT ((bbos_port_id_t) 0)
#define BBOS_PORT_IS_VALID(id) ((id) != BBOS_NULL_PORT)

typedef struct bbos_port_message {
	int id;
	size_t size;
	bbos_port_id_t feedback;
	struct bbos_port_message *next;
	void *data;
} bbos_port_message_t;

typedef struct bbos_port {
	bbos_port_message_t *first_message;
	bbos_port_message_t *last_message;
#ifdef BBOS_DEBUG
	bool_t init_complete;
#endif
} bbos_port_t;

/* Basic primitives */
bbos_return_t __bbos_port_init(bbos_port_id_t id);
bbos_return_t __bbos_port_write(bbos_port_id_t id, struct bbos_port_message *msg);
bbos_return_t	__bbos_port_read(bbos_port_id_t id, struct bbos_port_message *msg);
bool_t __bbos_port_is_empty(bbos_port_id_t id);

#define bbos_port_init(id) __bbos_port_init(id)
#define bbos_port_is_empty(id) __bbos_port_is_empty(id)
#define bbos_port_write(id, m) __bbos_port_write(id, m)
#define bbos_port_read(id, m) __bbos_port_read(id, m)

#endif

