/*
 * Messenger.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

/**
 * bbos_driver_receive - Receive a new message.
 * @port_id: Port identifier.
 *
 * Return value:
 *
 * Pointer to the message. See bbos_driver_msg structure.
 */
bbos_driver_msg_t
bbos_driver_receive(bbos_port_id_t port_id)
{
	return bbos_itc_receive(port_id);
}

bbos_return_t
bbos_driver_send()
{
}


