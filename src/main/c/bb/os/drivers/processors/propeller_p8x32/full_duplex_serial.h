#ifndef __FULL_DUPLEX_SERIAL_H
#define __FULL_DUPLEX_SERIAL_H

/**
 * Defines mode bits
 *   mode bit 0 = invert rx
 *   mode bit 1 = invert tx
 *   mode bit 2 = open-drain/source tx
 *   mode bit 3 = ignore tx echo on rx
 */
#define SERIAL_MODE_INVERT_RX      1
#define SERIAL_MODE_INVERT_TX      2
#define SERIAL_MODE_OPENDRAIN_TX   4
#define SERIAL_MODE_IGNORE_TX_ECHO 8

#include "types.h"

void full_duplex_serial_open(uint32_t rx_pin, uint32_t tx_pin,
                             uint32_t mode, uint32_t baudrate);
int full_duplex_serial_receive_byte();

#endif /* __FULL_DUPLEX_SERIAL_H */
