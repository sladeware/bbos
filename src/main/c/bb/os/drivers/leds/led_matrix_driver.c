/*
 * Copyright (c) 2013 Sladeware LLC
 */

#include "bb/os/drivers/leds/led_matrix_driver.h"
#include BBOS_PROCESSOR_FILE(pins.h)

void
open(void* cmd)
{
  int i;
  /* Set the 16 pins used to control the array as OUTPUTs */
  /* NOTE: it's user responsability to init first frame */
  for (i = 0; i < ((struct led_matrix_driver_cmd*)cmd)->num_rows; i++){
    DIR_OUTPUT(((struct led_matrix_driver_cmd*)cmd)->row_pins[i]);
  }
  for (i = 0; i < ((struct led_matrix_driver_cmd*)cmd)->num_cols; i++){
    DIR_OUTPUT(((struct led_matrix_driver_cmd*)cmd)->col_pins[i]);
  }
}

void
draw_frame(void* cmd, void* status)
{
  int d;
  int iii, col, i, row;
  unsigned char* frame = ((struct led_matrix_driver_cmd*)cmd)->frame;
  /* Show the current frame 'speed' times */
  for (iii = 0; iii < ((struct led_matrix_driver_cmd*)cmd)->speed; iii++) {
    for (col = 0; col < 8; col++) { /* Iterate through each column */
      /* Turn off all row pins */
      for (i = 0; i < 8; i++) {
        OUT_LOW(((struct led_matrix_driver_cmd*)cmd)->row_pins[i]);
      }
      for (i = 0; i < 8; i++) { /* Set only the one pin */
        if (i == col) {
          /* Turns the current row on */
          OUT_LOW(((struct led_matrix_driver_cmd*)cmd)->col_pins[i]);
        } else {
          /* Turns the rest of the rows off */
          OUT_HIGH(((struct led_matrix_driver_cmd*)cmd)->col_pins[i]);
        }
      }
      /* Iterate through each pixel in the current column */
      for (row = 0; row < ((struct led_matrix_driver_cmd*)cmd)->num_rows; row++) {
        /* If the bit in the frame array is set turn the LED on */
        if ((frame[col] >> row) & 1) {
          OUT_HIGH(((struct led_matrix_driver_cmd*)cmd)->row_pins[row]);
        }
      }
      /*
       * Leave the column on for few microseconds (too high a delay causes
       * flicker)
       */
      // BBOS_DELAY_MSEC(delay);
      for (d = 0; d < 500; d++);
    }
  }
  *(int8_t*)status = 1;
}
