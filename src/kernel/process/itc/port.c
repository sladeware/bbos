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

bbos_return_t
bbos_port_init(bbos_port_id_t id, struct bbos_mqueue *mq)
{
  bbos_port_table[id].mqueue = mqueue;
}

#endif /* BBOS_NUMBER_OF_PORTS > 0 */
