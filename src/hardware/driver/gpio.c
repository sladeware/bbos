/*
 * A "General Purpose Input/Output" (GPIO) is a flexible software-controlled
 * digital signal. Each GPIO represents a bit connected to a particular pin. 
 */

#include <bbos.h>

struct gpio_info {
  int8_t *label;
  int16_t base; // identifies the first GPIO number
  uint16_t n; // the number of GPIOs
};

/* Thread identifier for the GPIO driver should be defined manually. */
#ifndef GPIO_DRIVER_THREAD_ID
#error "GPIO thread identifier is undefined"
#endif

struct bbos_driver_local bbos_driver_local_table[BBOS_NUMBER_OF_DRIVERS];

enum {
  GPIO_DIRECTION_INPUT,
  GPIO_DIRECTION_OUTPUT
};

struct gpio_info {
  int8_t *label;
  int16_t base;
  uint16_t n; // number of pins
  uint16_t bitmap; // pins map
};

void
gpio()
{
  struct bbos_driver_message *message;
  struct gpio_info *gpio;
  bbos_driver_id_t id;

  bbos_itc_receive(&message, 0);
  id = message->id;

  gpio = (struct gpio_info *)bbos_driver_get_info(id);

  switch(message->cmd) {
  case BBOS_DRIVER_CMD_OPEN:
    // To open GPIO driver it should be closed first
    if(bbos_driver_local_table[id].state != BBOS_DRIVER_IS_CLOSED) {
      // error: driver is not closed
    }
    if((gpio->bitmap ^ *((uint16_t *)message->data)) <= gpio->bitmap) {
      // error: some of the required pins is already in use
    }
    break;
  }
}

bbos_return_t
gpio_is_valid(uin16_t base) {
  return (base < NUMBER_OF_GPIO);
}



