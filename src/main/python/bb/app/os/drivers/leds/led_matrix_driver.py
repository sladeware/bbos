# Copyright (c) 2013 Sladeware LLC

from bb.app.os import Driver

cmd_struct = [('speed', 4), ('frame', 4),
              ('num_rows', 4), ('row_pins', 4),
              ('num_cols', 4), ('col_pins', 4)]

class LEDMatrixDriver(Driver):
  name_format = 'LED_MATRIX_DRIVER_%d'
  runner = 'led_matrix_driver_runner'
  message_handlers = [
   ('open', ('BBOS_DRIVER_OPEN', cmd_struct)),
   ('draw_frame', ('DRAW_FRAME', cmd_struct),
                  ('DRAW_FRAME_STATUS', [('status', 1)])),
  ]
