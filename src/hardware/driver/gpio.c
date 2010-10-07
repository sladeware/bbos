/*
 * A "General Purpose Input/Output" (GPIO) is a flexible software-controlled
 * digital signal. Each GPIO represents a bit connected to a particular pin. 
 */

#include <bbos/hardware/driver/gpio.h>

/*
 * Describe GPIO table.
 */
struct gpio_pin *gpio_table[BBOS_HARDWARE_NUMBER_OF_GPIO_PINS];

struct gpio_request {
  uint16_t pin;
  int16_t value;
};

int16_t result;

/**
 * gpio_driver - Entry point for the thread which controls GPIO driver.
 */
void
gpio_driver()
{
  if (bbos_driver_messenger() != BBOS_SUCCESS) {
    return;
  }
}

void
bbos_driver_result(bbos_thread_id_t sender)
{
  bbos_itc_send(sender, &result);
}

void
bbos_driver_demultiplexer(bbos_driver_command_t command, void *data)
{
  struct gpio_request *request;

  /* Demultiplex standard commands */
  switch (command) {
  case BBOS_DRIVER_COMMAND(BBOS_DRIVER_COMMAND_OPEN):
    // This pin is already in use
    if (gpio_table[pin].owner != BBOS_UNKNOWN_THREAD_ID) {
      return;
    }
    gpio_table[pin].owner = sender;
    result = BBOS_SUCCESS;
    break;

  case BBOS_DRIVER_COMMAND(BBOS_DRIVER_COMMAND_CLOSE):
    if (gpio_table[pin].owner == BBOS_UNKNOWN_THREAD_ID) {
      // thread was not opened
      return;
    }
    gpio_table[pin].owner = BBOS_UNKNOWN_THREAD_ID;
    result = BBOS_SUCCESS;
    break;

  default:
    // Check owner of this pin
    if (gpio_table[pin].owner == BBOS_UNKNOWN_THREAD_ID) {
      // this pin wasn't opened so cannot be used
      return;
    }

    /* Let us take a look if this sender owns this pin */
    if (gpio_table[pin].owner != sender) {
      // error
      return;
    }
    break;
  }

  switch (command) {
  case BBOS_DRIVER_COMMAND(GPIO_DIRECTION_INPUT):
    result = GPIO_DIRECTION_INPUT(gpio_table[pin].chip, request->pin);
    break;

  case BBOS_DRIVER_COMMAND(GPIO_DIRECTION_OUTPUT):
    result = GPIO_DIRECTION_OUTPUT(gpio_table[pin].chip, request->pin, request->value);
    break;

  case BBOS_DRIVER_COMMAND(GPIO_SET_VALUE):
    result = GPIO_SET_VALUE(gpio_table[pin].chip, request->pin, request->value);
    break;

  case BBOS_DRIVER_COMMAND(GPIO_GET_VALUE):
    result = GPIO_GET_VALUE(gpio_table[pin].chip, request->pin);
    break;
  }
}

bbos_return_t
gpio_register_chip(struct gpio_chip *chip)
{
  uint16_t id;
  int16_t base;

  base = chip->base;

  /* Trace GPIO numbers so they must not be managed by another GPIO chip */
  for (id=base; id<base+chip->n; id++) {
    gpio_table[id] = chip;
  }

  return BBOS_SUCCESS;
}

bbos_return_t
gpio_unregister_chip(struct gpio_chip *chip)
{
  return BBOS_SUCCESS;
}



