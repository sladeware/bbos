
#include <bbos.h>

#if BBOS_NUMBER_OF_PORTS > 0

struct bbos_port bbos_port_table[BBOS_NUMBER_OF_PORTS];

void
bbos_port_init(bbos_port_id_t id, void *buffer, uint16_t size)
{
	assert(id < BBOS_NUMBER_OF_PORTS);

  bbos_port_table[id].buffer = buffer;
  bbos_port_table[id].size = size;
  bbos_port_table[id].in = bbos_port_table[id].out = 0;
}

/**
 * bbos_port_read - Read a data from the port to the buffer.
 */
uint16_t
bbos_port_read(bbos_port_id_t id, void *buffer, uint16_t n)
{
  uint16_t d;

	assert(id < BBOS_NUMBER_OF_PORTS);

  n = min(n, bbos_port_table[id].in - bbos_port_table[id].out);

  d = min(n, bbos_port_table[id].size - (bbos_port_table[id].out & 
    (bbos_port_table[id].size - 1)));
  memcpy(buffer, (void *)((uint16_t *)bbos_port_table[id].buffer + (bbos_port_table[id].out & (bbos_port_table[id].size - 1))), d);

  memcpy((void *)((uint16_t *)buffer + d), bbos_port_table[id].buffer, n - d);

  bbos_port_table[id].out += n;

  return n;
}

uint16_t
bbos_port_write(bbos_port_id_t id, void *buffer, uint16_t n)
{
  uint16_t d;

	assert(id < BBOS_NUMBER_OF_PORTS);

  n = min(n, bbos_port_table[id].size - bbos_port_table[id].in + 
    bbos_port_table[id].out);

  d = min(n, bbos_port_table[id].size - (bbos_port_table[id].in & 
    (bbos_port_table[id].size - 1)));
  memcpy((void *)((uint16_t *)bbos_port_table[id].buffer + (bbos_port_table[id].in & 
    (bbos_port_table[id].size - 1))), buffer, d);

  memcpy(bbos_port_table[id].buffer, (void *)((uint16_t *)buffer + d), n - d);

  bbos_port_table[id].in += n;

  return n;
}

void
bbos_port_flush(bbos_port_id_t id)
{
	assert(id < BBOS_NUMBER_OF_PORTS);

  bbos_port_table[id].in = bbos_port_table[id].out = 0;
}

int8_t
bbos_port_empty(bbos_port_id_t id)
{
	assert(id < BBOS_NUMBER_OF_PORTS);

	return (((bbos_port_table[id].in == 0) && (bbos_port_table[id].out == 0)) ? 1 : 0);
}

#endif /* BBOS_NUMBER_OF_PORTS > 0 */

