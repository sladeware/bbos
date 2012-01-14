/*
 * Start up to 7 cogs, then ping each one in turn
 */

#include <bb/os.h>
#include <bb/os/kernel/time.h>
#include <bb/mm/mempool.h>

#include <catalina_lmm.h>
#include <catalina_time.h>

/* define some global variables that all cogs will share: */
static int who;
static int lock;

/* define a default stack size to use for new cogs: */
#define STACK_SIZE 100

#define sync_printf(lock, frmt, arg)            \
  do {                                          \
    do { } while (_lockset(lock));              \
    t_printf(frmt, arg);                        \
    _lockclr(lock);                             \
  } while (0)

void
ping(void)
{
  int me = _cogid();

  sync_printf(lock, "Cog %d started!\n", me);
  while (1)
    {
      if (who == me)
        {
          sync_printf(lock, "... Cog %d pinged!\n", me);
          who = -1;
        }
    }
}

void
main()
{
  int i = 0;
  cog_id_t cog = 0;
  unsigned long stacks[STACK_SIZE * 7];
  bbos_thread_id_t tid;

  bbos();

  /* assign a lock to be used to avoid plugin contention */
  lock = _locknew();

  /* initialize ports */
  bbos_kernel_init_port(PORT0, 5, msgpool0);
  bbos_kernel_init_port(PORT1, 5, msgpool1);
  bbos_kernel_init_port(PORT2, 5, msgpool2);
  bbos_kernel_init_port(PORT3, 5, msgpool3);
  bbos_kernel_init_port(PORT4, 5, msgpool4);
  bbos_kernel_init_port(PORT5, 5, msgpool5);
  bbos_kernel_init_port(PORT6, 5, msgpool6);
  /* Application threads */
  for (tid = 0; tid < BBOS_CONFIG_NR_THREADS; tid++)
    {
      ping_me[tid] = BBOS_CONFIG_NR_THREADS - 1;
    }
  bbos_kernel_init_thread(THREAD0, thread0_runner, PORT0);
  cog = lmm_init_cog(&ping, &stacks[STACK_SIZE*(++i)]);
  bbos_kernel_init_thread(THREAD1, thread1_runner, PORT1);
  bbos_kernel_init_thread(THREAD2, thread2_runner, PORT2);
  bbos_kernel_init_thread(THREAD3, thread3_runner, PORT3);
  bbos_kernel_init_thread(THREAD4, thread4_runner, PORT4);
  bbos_kernel_init_thread(THREAD5, thread5_runner, PORT5);
  bbos_kernel_init_thread(THREAD6, thread6_runner, PORT6);
  bbos_kernel_enable_all_threads();
  bbos_kernel_start();

  /* start instances of ping_function until there are no cogs left */
  do
    {
      cog = lmm_new_cog(&ping, &stacks[STACK_SIZE*(++i)]);
    } while (cog >= 0);

  /* now loop forever, pinging each cog in turn */
  while (1)
    {
      for (cog = 0; cog < 8; cog++)
        {
          sync_printf(lock, "Pinging cog %d ...\n", cog);
          who = cog;
          /* slow things down a bit so we can see the messages */
          delay_ms(200);
        }
    }
}
