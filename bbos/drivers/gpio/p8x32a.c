/*
 * P8X32A GPIO driver.
 *
 * More details: http://forums.parallax.com/showthread.php?t=116370&page=20
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <stdio.h>
#include <bbos/kernel/hal/driver.h>
#include <bbos/drivers/gpio/p8x32a.h>

#define BIT(x) (1<<x)

/*******************************************************************************
 * P8X32A GPIO driver implentation with support of CATALINA compiler.
 ******************************************************************************/

#define P8X32A_GPIO_BANK(name, base, n) { name, base, n }

struct gpio_chip p8x32a_gpio_banks[] = {
  // Register A
  P8X32A_GPIO_BANK("A", 0, 32),
};

#ifdef __CATALINA__
#include <catalina_cog.h>

static int16_t
gpio_direction_input(unsigned int pin)
{
  unsigned int mask;
  struct gpio_chip *chip;

  chip = gpio_pin_to_chip(pin);
  mask = BIT(pin);

  // Register A
  if (chip->base == 0)
    {
      _dira(mask, 0);
      return BBOS_SUCCESS;
    }

  return BBOS_FAILURE;
}

static int16_t
gpio_get_value(unsigned int pin)
{
  return (_ina() & (1 << pin));
}

static int16_t
gpio_set_value(unsigned int pin, int bitval)
{
  unsigned int mask;
  unsigned int regval;
	
  regval = _ina();
  regval &= ~(!bitval << pin);   /* unset bit if bitval == 0 */
  regval |= (!!bitval << pin);   /* set bit if bitval == 1 */
  _outa(1<<pin, regval);
	
  return BBOS_SUCCESS;
}

static int16_t
gpio_direction_output(unsigned int pin, int level)
{
  unsigned int mask;
  struct gpio_chip *chip;
  
  chip = gpio_pin_to_chip(pin);
  mask = 1 << pin;

  _dira(mask, mask);
  gpio_set_value(pin, level);

  return BBOS_SUCCESS;
}

static void
bbos_driver_idle()
{
  /* NOP */
}

void
p8x32a_gpio_init(bbos_thread_id_t thread_id, bbos_port_id_t listen_port_id)
{
  // Introduce driver to the system.
  bbos_driver_bootstrapper(thread_id, listen_port_id);

  if (gpio_register_chip(&p8x32a_gpio_banks[0]) != 0) {
    printf("P8X32A GPIO driver can not initialize gpio banks.\n");
  }
}

void
p8x32a_gpio_messenger()
{
  /*
   * You can put here any additional code, which will be executed after the 
   * driver will be called.
   */
  bbos_driver_messenger();
}

#else
#error "Unsupported compiler."
#endif

static void
bbos_driver_demultiplexer(int command, void *data)
{
  struct gpio_message *request;

  request = (struct gpio_message *)data;

  switch (command)
  {
    case GPIO_OPEN:
			if (gpio_table[request->pin].owner != -1)	{
	  		/* Pin is already in use */
				request->error = BBOS_FAILURE;
				return;
			}
      gpio_table[request->pin].owner = request->owner;
      printf("Pin %d is owned by %d\n", request->pin, request->owner);
      request->error = BBOS_SUCCESS;
      return;
			
    case GPIO_CLOSE:
      if (gpio_table[request->pin].owner == -1) {
				/* Pin has no owner */
				request->error = BBOS_FAILURE;
	 			return;
			}
      gpio_table[request->pin].owner = -1;
      request->error = BBOS_SUCCESS;
      return;

    default:
      /* 
       * To get any other commands GPIO driver has to check your rights for the
       * particular pin.
       */
      if (gpio_table[request->pin].owner != request->owner) {
				request->error = BBOS_FAILURE;
				return;
			}
      break;
	}

  switch (command)
  {
    case GPIO_DIRECTION_INPUT:
      request->error = gpio_direction_input(request->pin);
    case GPIO_DIRECTION_OUTPUT:
      request->error = gpio_direction_output(request->pin, request->value);
    case GPIO_SET_VALUE:
      request->error = gpio_set_value(request->pin, request->value);
    case GPIO_GET_VALUE:
      request->error = gpio_get_value(request->pin);
    default:
      break;
	}
	
  request->error = BBOS_FAILURE;
}

