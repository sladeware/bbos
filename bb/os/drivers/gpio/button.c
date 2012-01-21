/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os/drivers/gpio/button.h>

/* Returns 1 when the button is pressed and 0 otherwise */
uint8_t is_button_pressed(uint8_t pin) {
  uint8_t result;
  uint8_t count;

  /* Read the push button state */
  for (count = 0, result = 0; count < DEBOUNCE_LOOPS; count++) {
    OUT_HIGH(pin);
    DIR_OUTPUT(pin);
    DIR_INPUT(pin);
    delay_ms(BUTTON_DELAY);
    result += GET_INPUT(pin);
  }

  return (result < DEBOUNCE_LOOPS);
}

