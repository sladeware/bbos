
#include <catalina_cog.h>
#include <stdio.h>

#define GET_PIN(p) (1<<p)
#define LED 2

static int mask = GET_PIN(LED);
static int on_off = GET_PIN(LED);

void
blink_runner()
{
  _dira(on_off, on_off);
  _outa(on_off, on_off);
  on_off ^= mask;
}

int
main()
{
  blink_runner();
  return 0;
}
