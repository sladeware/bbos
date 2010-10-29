
#include <bbos/hardware/driver/gpio.h>
#include <catalina_cog.h>

#define PROPELLER_GPIO_BANK(name, base, n)	\
  {						\
    name,					\
      n,					\
      base					\
      }

struct gpio_chip propeller_gpio_banks[] = {
  // Register A
  PROPELLER_GPIO_BANK("A", 0, 32),
};

void
gpio_init()
{
  int16_t i;

  for (i=0; i<1; i++) {
    gpio_register_chip(&propeller_gpio_banks[i]);
  }
}

void
gpio_exit()
{
}

void
GPIO_DIRECTION_INPUT(struct gpio_chip *chip, unsigned pin)
{
  unsigned int mask;

  mask = 1 << pin;

  switch (chip->base) {
    // Register A
  case 0:
    _dira(mask, 0);
    break;
    // Register B
    // (reserved)
  }

  return BBOS_SUCCESS;
}

void
GPIO_DIRECTION_OUTPUT(struct gpio_chip *chip, unsigned pin, int value)
{
  unsigned int mask;

  mask = 1 << pin;

  switch (chip->base) {
  case 0:
    /* Set pins to output */
    _dira(mask, mask);
    /* Set output */
    _outa(mask, value);
  }

  return BBOS_SUCCESS;
}

void
GPIO_GET_VALUE(struct gpio_chip *chip, unsigned int pin)
{
  unsigned int value;

  switch (chip->base) {
    // Register A
  case 0:
    value = _ina();
  }

  // take the pins in which we are interested in
  return (value & (1 << pin));
}

void
GPIO_SET_VALUE(struct gpio_chip *chip, unsigned int pin, int value)
{
  unsigned mask;

  mask = 1 << pin;

  switch (chip->base) {
  case 0:
    _outa(mask, value);
  }

  return BBOS_SUCCESS;
}
