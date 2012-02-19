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

unsigned button_driver_runner();
void controller_runner();
unsigned heater_driver_runner();
unsigned pump_driver_runner();
int temp_sensor_driver_water_runner();
int temp_sensor_driver_soil_a_runner();
int temp_sensor_driver_soil_b_runner();
int temp_sensor_driver_soil_c_runner();
int temp_sensor_driver_soil_d_runner();
void ui_runner();

#endif /* __VEGIMETER_H */
