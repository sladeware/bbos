/*
 * Port.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/*
 * The port interface will not be provided, unless at least 1 port will not be 
 * defined.
 */
#if BBOS_NUMBER_OF_PORTS > 0

struct bbos_port bbos_port_table[BBOS_NUMBER_OF_PORTS];

bbos_return_t
bbos_port_init(bbos_port_id_t id, struct bbos_mqueue *mq)
{
  bbos_port_table[id].mqueue = mqueue;
}

bbos_return_t
bbos_port_write(bbos_port_id_t id, void *)

bbos_return_t
bbos_port_destroy(bbos_port_id_t id)
{
}

#endif /* BBOS_NUMBER_OF_PORTS > 0 */

