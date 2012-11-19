/*
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
#ifndef __BB_OS_DRIVERS_GPIO_BUTTON_H
#define __BB_OS_DRIVERS_GPIO_BUTTON_H

#include <bb/os.h>
#include "button_driver_runner_autogen.h"

struct is_button_pressed_args {
  uint8_t pin;
  uint8_t* is_pressed;
};

struct are_buttons_pressed_args {
  uint16_t input_mask;
  uint16_t* output_mask;
};

#endif /* __BB_OS_DRIVERS_GPIO_BUTTON_H */