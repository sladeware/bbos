#!/usr/bin/env python

from bb.os.os import OS

TEST_CONFIG = '''
{"kernels": [{"threads": [{"runner": "engine_runner", "uid": 0, "port": "engine_port", "name": "engine"}]}, {"threads": [{"runner": "button_driver_runner", "uid": 1, "port": "button_driver_port", "name": "button_driver"}]}, {"threads": [{"runner": "led_matrix_driver_runner", "uid": 2, "port": "led_matrix_driver_port", "name": "led_matrix_driver"}]}], "max_message_size": 24, "messages": [{"fields": [["mask", 4]], "byte_size": 4, "label": "ARE_BUTTONS_PRESSED"}, {"fields": [["pin", 1]], "byte_size": 1, "label": "IS_BUTTON_PRESSED"}, {"fields": [["speed", 4], ["frame", 4], ["num_rows", 4], ["row_pins", 4], ["num_cols", 4], ["col_pins", 4]], "byte_size": 24, "label": "BBOS_DRIVER_OPEN"}, {"fields": [["mask", 4]], "byte_size": 4, "label": "PRESSED_BUTTONS"}, {"fields": [["status", 1]], "byte_size": 1, "label": "DRAW_FRAME_STATUS"}, {"fields": [["speed", 4], ["frame", 4], ["num_rows", 4], ["row_pins", 4], ["num_cols", 4], ["col_pins", 4]], "byte_size": 24, "label": "DRAW_FRAME"}, {"fields": [["pin", 1]], "byte_size": 1, "label": "PRESSED_BUTTON"}], "processor": {"family": "propeller_p8x32"}, "ports": [{"capacity": 10, "name": "engine_port", "uid": 0}, {"capacity": 10, "name": "led_matrix_driver_port", "uid": 2}, {"capacity": 10, "name": "button_driver_port", "uid": 1}]}
'''

OS.build_from_json(TEST_CONFIG)
