/*
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <catalina_time.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>

#ifndef __BUTTON_H
#define __BUTTON_H

#define BUTTON_DELAY       20  /* ms */
#define DEBOUNCE_LOOPS     50

uint8_t is_button_pressed(uint8_t pin);

#endif /* __BUTTON_H */
