/*
 * Copyright (c) 2012 Sladeware LLC
 */

/**
 * @file bb/os/drivers/onewire/onewire_bus.h
 * @brief One wire device I/O supportzz
 */

#ifndef __ONEWIRE_BUS_H
#define __ONEWIRE_BUS_H

#include <bbos.h>

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

#define OW_GET_INPUT()  (_ina() & ow_dpin)
#define OW_DIR_OUTPUT() (_dira(ow_dpin, ow_dpin))
#define OW_DIR_INPUT()  (_dira(ow_dpin, 0))
#define OW_OUT_LOW()    (_outa(ow_dpin, 0))
#define OW_OUT_HIGH()   (_outa(ow_dpin, ow_dpin))

/* Prototypes */

uint8_t ow_reset();

#define ow_read_byte() ow_io_byte(0xFF)
#define ow_write_byte(byte) ow_io_byte(byte)

uint8_t ow_io_byte(uint8_t byte);
uint8_t ow_io_bit(uint8_t bit);

#endif /* __ONEWIRE_BUS_H */
