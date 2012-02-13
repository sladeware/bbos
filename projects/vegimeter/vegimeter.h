/*
 * Copyright 2011 Sladeware LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef __VEGIMETER_H
#define __VEGIMETER_H

void button_driver_runner();
void controller_runner();
void heater_driver_runner();
void pump_driver_runner();
void temp_sensor_driver_water_runner();
void temp_sensor_driver_soil_a_runner();
void temp_sensor_driver_soil_b_runner();
void temp_sensor_driver_soil_c_runner();
void temp_sensor_driver_soil_d_runner();
void ui_runner();

/* Shared global variables. Written by drivers and read by the controller thread. The
   controller clears the buttons_pressed and drivers OR values. */
static unsigned vegimeter_buttons = 0;
static float water_temperature = 0.0;
static float soil_temperature_a = 0.0;
static float soil_temperature_b = 0.0;
static float soil_temperature_c = 0.0;
static float soil_temperature_d = 0.0;
static unsigned heater_on = 0;
static unsigned pump_on = 0;

#endif /* __VEGIMETER_H */
