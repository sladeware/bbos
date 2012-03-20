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

#include <bb/os.h>

#ifndef __BUTTON_H
#define __BUTTON_H

#define BUTTON_DELAY       4    /* ms */
#define BUTTON_FINAL_DELAY 100  /* ms */
#define DEBOUNCE_LOOPS     60
#define DEBOUNCE_TOLERANCE 15

uint8_t is_button_pressed(uint8_t pin);
uint16_t are_buttons_pressed(uint16_t mask);

#endif /* __BUTTON_H */
