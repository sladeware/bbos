/*
 * This file implements button.h interface
 *
 * Copyright (c) 2012 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "button.h"

#include <bb/os/kernel/delay.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>

#define BUTTON_DELAY 4 /* ms */
#define BUTTON_FINAL_DELAY 100 /* ms */
#define DEBOUNCE_LOOPS 60
#define DEBOUNCE_TOLERANCE 15

/*
 * Input argument is the button pin scanned. Returns 1 when the button is
 * pressed and 0 otherwise.
 */
void
is_button_pressed(void* args)
{
  uint8_t pin;
  uint8_t result;
  uint8_t count;
  pin = ((struct is_button_pressed_args*)args)->pin;
  /* Read the push button state */
  for (count = 0, result = 0; count < DEBOUNCE_LOOPS; count++) {
    OUT_HIGH(pin);
    DIR_OUTPUT(pin);
    DIR_INPUT(pin);
    BBOS_DELAY_MSEC(BUTTON_DELAY);
    result += GET_INPUT(pin);
  }
  BBOS_DELAY_MSEC(BUTTON_FINAL_DELAY);
  *((struct is_button_pressed_args*)args)->is_pressed = (result < (DEBOUNCE_LOOPS - DEBOUNCE_TOLERANCE));
}

/*
 * Input argument is a bit mask of buttons scanned. Returns a bit
 * mask of the buttons that were pressed.
 *
 * TODO: run this function from HUB if compiled for LMM.
 *
 * NOTE(Slade): see another implementation from demos for propgcc in
 * demos/forumists/jazzed/QSwam/qswam.c
 */
void
are_buttons_pressed(void* args)
{
  uint32_t result[32];
  uint32_t output;
  uint8_t count;
  uint8_t pin;
  uint16_t mask;

  mask = ((struct are_buttons_pressed_args*)args)->input_mask;

  for (pin = 0; pin < 32; pin++) {
    result[pin] = 0;
  }
  /* Read the push button state */
  for (output = 0, count = 0; count < DEBOUNCE_LOOPS; count++) {
    OUT_HIGH_MASK(mask);
    DIR_OUTPUT_MASK(mask);
    DIR_INPUT_MASK(mask);
    BBOS_DELAY_MSEC(BUTTON_DELAY);

    output = GET_INPUT_MASK(mask);
    for (pin = 0; (output > 0) && (pin < 32); pin++, output >>= 1) {
      if (output & 1UL) {
        result[pin]++;
      }
    }
  }
  BBOS_DELAY_MSEC(BUTTON_FINAL_DELAY);
  OUT_LOW_MASK(mask);
  DIR_INPUT_MASK(mask);
  /* Process the results and return the mask of pressed buttons */
  for (pin = 0, output = 0; pin < 32; pin++) {
    if ((result[pin] > 0)
        && (result[pin] < (DEBOUNCE_LOOPS - DEBOUNCE_TOLERANCE))) {
      output |= 0x80000000UL;
    }
    if (pin < 31) {
      output >>= 1;
    }
  }
  *((struct are_buttons_pressed_args*)args)->output_mask = output;
}

#include "button_driver_runner_autogen.c"
