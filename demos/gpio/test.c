/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/kernel.h>
#include <bbos/kernel/port.h>

#ifdef __CATALINA__
#include <catalina_cog.h>
#endif

#include <bbos/drivers/gpio/p8x32a.h>

#define PIN 18

void 
blinker() 
{
  static struct bbos_port_message message;
  static bool_t init_complete = FALSE;
  static struct gpio_message request;
  static uint32_t mask = 1 << PIN;
  static uint32_t indicator = 1 << PIN;

  if (!bbos_port_is_empty(BLINKER_PORT_ID))
    {
      bbos_port_read(BLINKER_PORT_ID, &message);
      request = *(struct gpio_message *)message.data;

      switch (message.id)
	{
	case GPIO_OPEN:
	  if (request.error == BBOS_SUCCESS)
	    {
	      printf("Pin %d was successfully owned.\n", PIN);
	      init_complete = TRUE;
	    }
	  else
	    printf("Cannot open required pin: %d\n", request.error);
	  break;
	case GPIO_DIRECTION_OUTPUT:
	  if (request.error == BBOS_SUCCESS)
	    printf("Output direction was set\n");
	  else
	    printf("Cannot set output direction: %d\n", request.error);
	  break;
	}
    }

  if (!init_complete)
    {
      request.pin = PIN;
      request.value = indicator;

      message.id = GPIO_OPEN;
      message.data = &request;
      message.feedback = BLINKER_PORT_ID;

      bbos_port_write(GPIO_PORT_ID, &message);

      return;
    }
	
  // OK, let us make some blink :)
  request.pin = PIN;
  request.value = indicator;
  indicator ^= mask; // turn on/off desired pin

  message.id = GPIO_DIRECTION_OUTPUT;
  message.data = &request;
	
  bbos_port_write(GPIO_PORT_ID, &message);
}

void
bbos()
{
//	_clockinit(PLL16X, _clockfreq());


  bbos_port_init(BLINKER_PORT_ID);
  bbos_port_init(GPIO_PORT_ID);

  gpio_driver_init(0, GPIO_PORT_ID); // TODO: UNKNOWN_THREAD

  /* Clear DIRA and OUTA registers */
  _dira(0xFF0000, 0xFF0000);
  _outa(0xFF0000, 0xFF0000);
  bbos_delay_msec(500);
  _outa(0xFF0000, 0);
  //_dira(0xFF0000, 0);
  
  while (1)
    {
      blinker();
      gpio_driver_messenger();
      bbos_delay_msec(500);
    }
}

