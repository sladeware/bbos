/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <catalina_time.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>

#ifndef __BUTTON_H
#define __BUTTON_H

#define BUTTON_DELAY       4    /* ms */
#define BUTTON_FINAL_DELAY 100  /* ms */
#define DEBOUNCE_LOOPS     60
#define DEBOUNCE_TOLERANCE 15

uint8_t is_button_pressed(uint8_t pin);
unsigned are_buttons_pressed(unsigned mask);

#endif /* __BUTTON_H */
