
#include <bbos.h>

#if BBOS_NUMBER_OF_PORTS > 0

struct bbos_port bbos_port_table[BBOS_NUMBER_OF_PORTS];

void
bbos_port_init(bbos_port_id_t id, uint8_t *buffer, uint16_t size)
{
  bbos_port_table[id].buffer = buffer;
  bbos_port_table[id].size = size;
  bbos_port_table[id].in = bbos_port_table[id].out = 0;
}

/**
 * bbos_port_read - Read a data from the port to the buffer.
 */
uint16_t
bbos_port_read(bbos_port_id_t id, uint8_t *buffer, uint16_t n)
{
  uint16_t d;

  n = min(n, bbos_port_table[id].in - bbos_port_table[id].out);

  d = min(size, bbos_port_table[id].size - (bbos_port_table[id].out & 
    (bbos_port_table[id].size - 1)));
  memcpy(buffer, bbos_port_table[id].buffer + (bbos_port_table[id].out &
    (bbos_port_table[id].size - 1)), d);

  memcpy(buffer + d, bbos_port_table[id].buffer, n - d);

  bbos_port_table[id].out += n;

  return n;
}

uint16_t
bbos_port_write(bbos_port_id_t id, uint8_t *buffer, uint16_t n)
{
  uint16_t d;

  n = min(n, bbos_port_table[id].size - bbos_port_table[id].in + 
    bbos_port_table[id].out);

  d = min(n, bbos_port_table[id].size - (bbos_port_table[id].in & 
    (bbos_port_table[id].size - 1)));
  memcpy(bbos_port_table[id].buffer + (bbos_port_table[id].in & 
    (bbos_port_table[id].size - 1)), buffer, d);

  memcpy(bbos_port_table[id].buffer, bbos_port_table[id].buffer + d, n - d);

  bbos_port_table[id].in += n;

  return n;
}

void
bbos_port_flush(bbos_port_id_t id)
{
  bbos_port_table[id].in = bbos_port_table[id].out = 0;
}

#endif

