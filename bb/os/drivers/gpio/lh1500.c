/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/os/drivers/gpio/lh1500.h>

void lh1500_on(uint8_t pin) {
  OUT_HIGH(pin);
  DIR_OUTPUT(pin);
}

void lh1500_off(uint8_t pin) {
  OUT_LOW(pin);
  DIR_OUTPUT(pin);
}
