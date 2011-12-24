/*
 * WARNING: this file was automatically generated!
 */
#ifndef __P8X32_SERIAL_H
#define __P8X32_SERIAL_H

#include <bb/os.h>

/* List devices */
#define P8X32_SERIAL P8X32_SERIAL
#define P8X32_SERIAL_ID 0

#include "p8x32_serial_interface.h"

/* Prototypes */
void P8X32_SERIALserial_open(bbos_device_id_t dev_id, uint32_t rx_pin, uint32_t tx_pin, 
    uint32_t mode, uint32_t baudrate);

#endif


