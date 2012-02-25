/*
 * The "Blink me who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 */
#include <stdio.h>
#include <unistd.h>
#include <propeller.h>

int
main()
{
//#ifdef __CATALINA_DEMO

//#else /* __CATALINA_DEMO */
//#error This board is not supported
//#endif

//  sleep(5);

  _DIRA |= 0x00FF0000;

 _OUTA = 1 << (16 + cogid());
  for (;;)
    {
    }

      /* Flush LED that corresponds to active cog. */
      //reg = _dira(0, 0);
      //_dira(led_mask, (reg & led_mask) ^ led_mask);
      //reg = _outa(0, 0);
      //_outa(led_mask, (reg & led_mask) ^ led_mask);
      //msleep(500); /* wait... */
//    }
  return 0;
}
