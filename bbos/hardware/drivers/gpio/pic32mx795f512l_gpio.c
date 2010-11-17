
#include <bbos/hardware/drivers/hal.h>

#define PIC32MX795F512L_GPIO_BANK(name, base, n) { name, base, n }

struct bbos_gpio_chip pic32mx795f512l_gpio_banks[] = {
	// Port A
	PIC32MX795F512L_GPIO_BANK("A",  0,  8),
	PIC32MX795F512L_GPIO_BANK("A",  9,  2),
	PIC32MX795F512L_GPIO_BANK("A", 14,  2),
  // Port B
	PIC32MX795F512L_GPIO_BANK("B", 16, 16),
	// Port C
	PIC32MX795F512L_GPIO_BANK("C", 33,  4),
	PIC32MX795F512L_GPIO_BANK("C", 44,  4),
	// Port D
	PIC32MX795F512L_GPIO_BANK("D", 48, 16),
	// Port E
	PIC32MX795F512L_GPIO_BANK("E", 64, 10),
	// Port F
	PIC32MX795F512L_GPIO_BANK("F", 80,  6),
	PIC32MX795F512L_GPIO_BANK("F", 88,  1),
	PIC32MX795F512L_GPIO_BANK("F", 91,  2),
	// Port G
	PIC32MX795F512L_GPIO_BANK("G", 96,  4),
	PIC32MX795F512L_GPIO_BANK("G", 96, 16),
};

static bbos_return_t
gpio_direction_input(unsigned int pin)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;
  
  return BBOS_SUCCESS;
}

static bbos_return_t
gpio_direction_output(unsigned int pin, int value)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;
  
  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;

  return BBOS_FAILURE;
}

static bbos_return_t
gpio_get_value(unsigned int pin)
{
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);
  
  return BBOS_FAILURE;
}

static bbos_return_t
gpio_set_value(unsigned int pin, int value)
{
  unsigned int mask;
  struct bbos_gpio_chip *chip;

  chip = bbos_gpio_pin_to_chip(pin);
  mask = 1 << pin;
 
  return BBOS_FAILURE;
}

void
pic32mx795f512l_gpio_init()
{
  /* Register GPIO chips */
  if (bbos_gpio_register_chip(pic32mx795f512l_gpio_banks) != BBOS_SUCCESS) {
    bbos_panic("P8X32A GPIO driver can not initialize gpio banks.\n");
  }
}


