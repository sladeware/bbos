/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/onewire/onewire_bus.h
 * @brief One wire device I/O support
 */

#ifndef __ONEWIRE_BUS_H
#define __ONEWIRE_BUS_H

#include <bb/os.h>
#include <bb/builder/compilers/catalina/include/catalina_time.h>
#include <catalina_time.h>

// ROM commands
/** Read the 64-bit ID of the 1-Wire device;serial num; CRC */
#define OW_READ_ROM 0x33
/** Look for specific device */
#define OW_MATCH_ROM 0x55
/** Skip rom (one device)  */
#define OW_SKIP_ROM 0xCC
/** Search */
#define OW_SEARCH_ROM 0xF0
#define OW_ALARM_SEARCH_ROM 0xEC

/* Remember that pins start at 0 */
#define GET_OW_DPIN(pin) (1 << pin)

#define OW_GET_INPUT(pin)  (_ina() & GET_OW_DPIN(pin))
#define OW_DIR_OUTPUT(pin) (_dira(GET_OW_DPIN(pin), GET_OW_DPIN(pin)))
#define OW_DIR_INPUT(pin)  (_dira(GET_OW_DPIN(pin), 0))
#define OW_OUT_LOW(pin)    (_outa(GET_OW_DPIN(pin), 0))
#define OW_OUT_HIGH(pin)   (_outa(GET_OW_DPIN(pin), GET_OW_DPIN(pin)))

#if 1
/* Sleep macro */
#define ow_delay_usec(usecs) (_waitcnt(_cnt() + usecs * (_clockfreq() / 1000000)))
#endif

/* Prototypes */

uint8_t ow_reset(uint8_t pin);

#define ow_read_byte(pin) ow_io_byte(0xFF, pin)
#define ow_write_byte(byte, pin) ow_io_byte(byte, pin)

uint8_t ow_io_byte(uint8_t byte, uint8_t pin);
uint8_t ow_io_bit(uint8_t bit, uint8_t pin);

uint8_t ow_input_pin_state(uint8_t pin);
void ow_command(uint8_t cmd, uint8_t pin);

#endif /* __ONEWIRE_BUS_H */
