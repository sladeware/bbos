/*
 * Process.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>

/*
 * At least one thread should always exist, which means BBOS_NUMBER_OF_THREADS 
 * always > 0. Just a test.
 */
#if BBOS_NUMBER_OF_THREADS > 0

bbos_thread_t bbos_process_thread_table[BBOS_NUMBER_OF_THREADS];

/**
 * bbos_process_init_threads - Initialize threads within process.
 *
 * Description:
 *
 * By default each thread doesn't support ITC mechanism and it has the lowest 
 * priority defined as BBOS_THREAD_LOWEST_PRIORITY. See bbos_thread_init().
 */
void
bbos_process_init_threads()
{
  bbos_thread_id_t tid;

  for(tid=0; tid < BBOS_NUMBER_OF_THREADS; tid++) {
		bbos_thread_init(tid);
  }
}

#endif /* BBOS_NUMBER_OF_THREADS > 0 */

/*
 * The number of ports within a process should not be always > 0. In the case 
 * when the number of ports is zero, BBOS decides to do not support thread 
 * communication mechanisms.
 */
#if BBOS_NUMBER_OF_PORTS > 0

bbos_port_t bbos_process_port_table[BBOS_NUMBER_OF_PORTS];

/**
 * bbos_process_init_ports - Initialize ports.
 */
void
bbos_process_init_ports()
{
}

#endif /* BBOS_NUMBER_OF_PORTS > 0 */

/*
 * The system could also do not have device drivers.
 */
#if BBOS_NUMBER_OF_DEVICE_DRIVERS > 0

bbos_device_driver_t bbos_process_device_driver_table[BBOS_NUMBER_OF_DEVICE_DRIVERS];

/**
 * bbos_process_init_device_drivers - Initialize device drivers.
 */
void
bbos_process_init_device_drivers()
{
  bbos_device_driver_id_t device_id;

  for(device_id=0; device_id<BBOS_NUMBER_OF_DEVICE_DRIVERS; device_id++) {
    //bbos_device_driver_unregister(device_id);
  }
}

#endif /* BBOS_NUMBER_OF_DEVICE_DRIVERS > 0 */

/**
 * bbos_process_init - Initialize process.
 */
void
bbos_process_init()
{
	/* Initialize ports if the process have them */
#if BBOS_NUMBER_OF_PORTS > 0
    bbos_process_init_ports();
#endif

	/* Initialize device drivers if the process have them */
#if BBOS_NUMBER_OF_DEVICE_DRIVERS > 0
    bbos_process_init_device_drivers();
#endif

    bbos_process_init_threads();

    /* Initialize scheduler */
    bbos_sched_init();
}

/**
 * bbos_process_start - Start process.
 */
void
bbos_process_start()
{
  bbos_sched_loop();
}

/**
 * bbos_process_stop - Stop process.
 */
void
bbos_process_stop()
{
}

