/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os/drivers/gpio/button.h>

/* Returns 1 when the button is pressed and 0 otherwise */
uint8_t is_button_pressed(uint8_t pin) {
  uint8_t result;

  /* Read the push button state */
  DIR_INPUT(pin);
  result = GET_INPUT(pin);

  /* Wait a little while to debounce */
  delay_ms(DEBOUNCE_DELAY);

  /* If it is still high then return 1, else return 0 */
  return (result & GET_INPUT(pin));
}

