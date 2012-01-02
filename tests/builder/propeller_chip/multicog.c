/*
 * Start up to 7 cogs, then ping each one in turn
 */

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

  /* assign a lock to be used to avoid plugin contention */
  lock = _locknew();

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
