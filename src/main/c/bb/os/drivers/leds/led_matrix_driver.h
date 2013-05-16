#ifndef __LED_MATRIX_DRIVER_H
#define __LED_MATRIX_DRIVER_H

struct led_matrix_driver_cmd {
  /* Number of times to repeat each frame */
  int speed;
  unsigned num_rows;
  /*
   * An array defining which pin each row is attached to (rows are common anode
   * (drive HIGH)).
   */
  int* row_pins;
  unsigned num_cols;
  /*
   * An array defining which pin each column is attached to (columns are common
   * cathode (drive LOW)).
   */
  int* col_pins;
  /*
   * The array used to hold a bitmap of the display (if you wish to do something
   * other than scrolling marque change the frame in this variable then
   * display).
   */
  unsigned char* frame;
};

#endif /* __LED_MATRIX_DRIVER_H */
