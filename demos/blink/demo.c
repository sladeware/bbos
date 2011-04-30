
#include <stdio.h>
#include <bbos/kernel.h>

#include <catalina_cog.h>

#define PIN(i) (1<<(i))

static int mask = PIN(27);
static int on_off = PIN(27);

void
wait(int milliseconds)
{
  _waitcnt(_cnt() + milliseconds *(_clockfreq()/1000));
}

void blink()
{
  _dira(mask, on_off);
  _outa(mask, on_off);
  wait(200);

  on_off ^= mask;
}

void main()
{
  bbos_init();
  bbos_start_thread(BLINK, blink);
  bbos_start();
}

