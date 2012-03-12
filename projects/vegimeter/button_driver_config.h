/*
 * Copyright 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define BBOS_SKIP_BANNER_PRINTING
#define BBOS_CONFIG_PROCESSOR propeller_p8x32
#define BBOS_CONFIG_NR_THREADS 7

#define SIO_COGSAFE_PRINTING
#define SIO_PRINTF_STRING_SUPPORT
#define bbos_printf sio_printf

/* Define shared memory space */
#define VEGIMETER_SHMEM_ADDR 24576 /* 24K */
#define VEGIMETER_BUTTONS_ADDR (VEGIMETER_SHMEM_ADDR)

#define BBOS_CONFIG_USE_STATIC_SCHED
#define bbos_main()
#define BBOS_CONFIG_KERNEL_LOOP  /* see button_driver.c */

/*
#define BBOS_NR_PORTS 2
#define BBOS_CONFIG_MESSAGING_POOL_SIZE (BBOS_CONFIG_NR_THREADS * BBOS_CONFIG_NR_THREADS)
*/