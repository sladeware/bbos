/*
 * Copyright (c) 2011 Sladeware LLC
 */
#ifndef __P8X32_UART_H
#define __P8X32_UART_H

#include <bb/os/kernel.h>

#define SERIAL_BUFF_MASK 0xf

/**
 * Defines mode bits
 *   mode bit 0 = invert rx
 *   mode bit 1 = invert tx
 *   mode bit 2 = open-drain/source tx
 *   mode bit 3 = ignore tx echo on rx
 */
#define SERIAL_MODE_INVERT_RX 1
#define SERIAL_MODE_INVERT_TX 2
#define SERIAL_MODE_OPENDRAIN_TX 4
#define SERIAL_MODE_IGNORE_TX_ECHO 8

/* Prototypes */

PROTOTYPE(void serial_open, (unsigned long rx_pin, unsigned long tx_pin,
                             unsigned long mode, unsigned long baudrate));
PROTOTYPE(int serial_wait, (void));
PROTOTYPE(int serial_send_byte, (int byte));
PROTOTYPE(int serial_receive_byte, ());
PROTOTYPE(void serial_flush, ());
PROTOTYPE(int serial_timeout, (unsigned long ms));

#endif /* __P8X32_UART_H */
