/*
 * Bootstrapper.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

bbos_return_t
bbos_driver_bootstrap()
{
	bbos_driver_id_t drv_id;

	drv_id = bbos_sched_myself;

	bbos_process_driver_table[drv_id].owner = bbos_sched_myself;
	
}

