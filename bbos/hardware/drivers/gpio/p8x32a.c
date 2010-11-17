/*
 * P8X32A GPIO programming interface. This interface works with optional 
 * library for GPIO interfaces.
 *
 * P8X32A GPIO Driver:
 *
 * (!)	P8X32A_GPIO_ID - thread identifier.
 * (!)	P8X32A_GPIO_PORT_ID - port identifier for communication.
 * 			P8X32A_GPIO_PORT_SIZE - port size in bytes.
 *
 * Where (!) means that this value should be set by user/builder.
 *
 * P8X32A GPIO Driver Commands:
 *
 * Please, see the basic list of commands with their description for a GPIO 
 * driver in gpio.h header file, where the basic commands are:
 *
 * 		BBOS_GPIO_OPEN/BBOS_DRIVER_OPEN
 * 		BBOS_GPIO_CLOSE/BBOS_DRIVER_CLOSE
 *
 * 		BBOS_GPIO_DIRECTION_INPUT
 *		BBOS_GPIO_DIRECTION_OUTPUT
 *		BBOS_GPIO_SET_VALUE
 *		BBOS_GPIO_GET_VALUE
 *
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>
#include <bbos/hardware/drivers/gpio/p8x32a.h>
#include <bbos/hardware/drivers/hal.h>

#ifndef P8X32A_GPIO_ID
#error "P8X32A GPIO driver identifier was not set."
#endif

#ifndef P8X32A_GPIO_PORT_ID
#error "P8X32A GPIO port identifier was not set."
#endif

#ifndef P8X32A_GPIO_PORT_NUMBER_OF_MESSAGES
#define P8X32A_GPIO_PORT_NUMBER_OF_MESSAGES 5
#endif

#define P8X32A_GPIO_PORT_SIZE (P8X32A_GPIO_PORT_NUMBER_OF_MESSAGES \
	* sizeof(bbos_driver_request))

int8_t p8x32a_gpio_port[P8X32A_GPIO_PORT_SIZE];

#define P8X32A_GPIO_BANK(name, base, n) { name, base, n }

struct bbos_gpio_chip p8x32a_gpio_banks[] = {
	// Register A
	P8X32A_GPIO_BANK("A", 0, 32),
};

/* P8X32A GPIO driver implentation with support of catalina compiler. */
#ifdef __CATALINA__
#include <catalina_cog.h>

static bbos_return_t
gpio_direction_input(unsigned int pin)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;

  // Register A
  if (chip->base == 0) {
    _dira(mask, 0);
    return BBOS_SUCCESS;
  }

  return BBOS_FAILURE;
}

static bbos_return_t
gpio_direction_output(unsigned int pin, int value)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;
  
  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;

  if (chip->base == 0) {
    _dira(mask, mask);    /* Set pins to output */
    _outa(mask, value);   /* Set output */
    return BBOS_SUCCESS;
  }

  return BBOS_FAILURE;
}

static bbos_return_t
gpio_get_value(unsigned int pin)
{
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);

  if (chip->base == 0) {
    // get value and take pins in which we are insterested id
//    *(bbos_driver_response.data) = (_ina() & (1 << pin));
    bbos_driver_response.size = sizeof(unsigned int);
    return BBOS_SUCCESS;
  }
	
  return BBOS_FAILURE;
}

static bbos_return_t
gpio_set_value(unsigned int pin, int value)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;

  if (chip->base == 0) {
    _outa(mask, value);
    return BBOS_SUCCESS;
  }

  return BBOS_FAILURE;
}

#else
#error "Unsupported compiler."
#endif

/**
 * bbos_driver_command - Process driver commands.
 */
static bbos_return_t
bbos_driver_command()
{
  struct bbos_gpio_message *request;

  request = (struct bbos_gpio_message *)bbos_driver_request.data;

  switch (bbos_driver_request.command) {
  case BBOS_DRIVER_OPEN:
    if (bbos_gpio_table[request->pin].owner != BBOS_UNKNOWN_ID) {
      /* Pin is already in use */
      return BBOS_FAILURE;
    }
    bbos_gpio_table[request->pin].owner = bbos_driver_request.sender;
    return BBOS_SUCCESS;
			
  case BBOS_DRIVER_CLOSE:
    if (bbos_gpio_table[request->pin].owner == BBOS_UNKNOWN_ID) {
      /* Pin has no owner */
      return BBOS_FAILURE;
    }
    bbos_gpio_table[request->pin].owner = BBOS_UNKNOWN_ID;
    return BBOS_SUCCESS;

  default:
    /* 
     * To get any other commands GPIO driver has to check your rights for the
     * particular pin.
     */
    if (bbos_gpio_table[request->pin].owner != bbos_driver_request.sender) {
      return BBOS_FAILURE;
    }
    break;
  }

  switch (bbos_driver_request.command) {
  case BBOS_GPIO_DIRECTION_INPUT:
    return gpio_direction_input(request->pin);
  case BBOS_GPIO_DIRECTION_OUTPUT:
    return gpio_direction_output(request->pin, request->value);
  case BBOS_GPIO_SET_VALUE:
    return gpio_set_value(request->pin, request->value);
  case BBOS_GPIO_GET_VALUE:
    return gpio_get_value(request->pin);
  default:
    break;
  }
	
  return BBOS_FAILURE;
}

/**
 * p8x32a_gpio_init - Initialize GPIO driver.
 *
 * Description:
 *
 * Register known GPIO banks for P8X32A chip.
 */
void
p8x32a_gpio_init()
{
  /* Register GPIO chips */
  if (bbos_gpio_register_chip(&p8x32a_gpio_banks[0]) != BBOS_SUCCESS) {
    bbos_panic("P8X32A GPIO driver can not initialize gpio banks.\n");
  }

  /* Register driver */
  //bbos_driver_register(P8X32A_GPIO_ID, "P8X32A_GPIO", 0, "");

  /* Initalize P8X32 GPIO driver communication mechanisms */	
  bbos_port_init(P8X32A_GPIO_PORT_ID, p8x32a_gpio_port, P8X32A_GPIO_PORT_SIZE);

  /* Initialize and start schedule GPIO driver */
  bbos_driver_register(P8X32A_GPIO_ID, P8X32A_GPIO_PORT_ID);
}

