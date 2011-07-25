
#include <stdio.h>
#include <bbos/kernel.h>

#include <catalina_cog.h>

#define PIN(i) (1<<(i))

void
wait(int milliseconds)
{
  _waitcnt(_cnt() + milliseconds *(_clockfreq()/1000));
}

void helloworld()
{

}

void main()
{
  static int mask;
  static int on_off;

  bbos_init();

  // Clear DIRA and OUTA registers
  _dira(0xFFFFFFFF, 0xFFFFFFFF); // 0-31 GPIO pin
  _outa(0xFFFFFFFF, 0);

  mask = PIN(18);
  on_off = mask;

  while (1)
    {
      _dira(mask, on_off);
      _outa(mask, on_off);
      wait(1000);

      on_off ^= mask;
    }  

  //bbos_start_thread(HELLOWORLD, helloworld);
  //bbos_start();
}

