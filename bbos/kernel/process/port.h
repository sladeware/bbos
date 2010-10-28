/*
 * Copyright (c) ???? Slade Maurer, Alexander Sviridenko
 *
 */
#ifndef __BBOS_PORT_H
#define __BBOS_PORT_H

#if BBOS_NUMBER_OF_PORTS > 0

#define bbos_port_get_input(id)   bbos_port_table[id].in
#define bbos_port_get_output(id)  bbos_port_table[id].out

typedef int16_t bbos_port_id_t;

struct bbos_port {
  uint8_t *buffer;
  uint16_t in;
  uint16_t out;
  uint16_t size;
};

extern struct bbos_port bbos_port_table[BBOS_NUMBER_OF_PORTS];

void bbos_port_init(bbos_port_id_t id, uint8_t *buffer, uint16_t size);
uint16_t bbos_port_read(bbos_port_id_t id, uint8_t *buffer, uint16_t n);
bbos_uint16_t bbos_port_write(bbos_port_id_t id, uint8_t *buffer, uint16_t n);
void bbos_port_flush(bbos_port_id_t id);

#else
#define BBOS_NUMBER_OF_PORTS 0
#endif /* BBOS_NUMBER_OF_PORTS > 0 */

#endif /* __BBOS_PORT_H */

