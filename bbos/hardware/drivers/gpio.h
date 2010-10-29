/*
 * GPIO programming interface.
 */

#include <bbos.h>

/*
 * BBOS_HARDWARE_NUMBER_OF_GPIO_PINS defines valid GPIO numbers to be in the range
 * 0..MAX_INT, this library restricts them to the smaller range
 * 0..BBOS_HARDWARE_NUMBER_OF_GPIO_PINS-1.
 */
#ifndef BBOS_HARDWARE_NUMBER_OF_GPIO_PINS
#define BBOS_HARDWARE_NUMBER_OF_GPIO_PINS 256
#endif

struct gpio_chip {
  char *label;
  int base; // the first pin number
  unsigned int n; // the number of pins handled by this chip
};

struct gpio_pin {
  struct gpio_chip *chip; // chip to which this pin belongs
  bbos_thread_id_t owner; // thread which owns this pin
};

#define BBOS_DRIVER_COMMAND(name) _dc_ ## name

/* TODO: Fixup these values, so they should not lay over the standard commands */
enum gpio_commands {
  BBOS_DRIVER_COMMAND(GPIO_DIRECTION_INPUT),
  BBOS_DRIVER_COMMAND(GPIO_DIRECTION_OUTPUT),
  BBOS_DRIVER_COMMAND(GPIO_SET_VALUE),
  BBOS_DRIVER_COMMAND(GPIO_GET_VALUE)
};

