/*
 * WARNING: this file was automatically generated!
 */

#define OK

/* Include main header file */
#include "p8x32_serial.h"

/* Prepare control interface */
#define serial_open(...)        BBOS_CONTROL_DEVICE(P8X32_SERIAL, serial_open, __VA_ARGS__)
#define serial_close(...)       BBOS_CONTROL_DEVICE(P8X32_SERIAL, serial_close, __VA_ARGS__)
#define serial_transmit(...)    BBOS_CONTROL_DEVICE(P8X32_SERIAL, serial_transmit, __VA_ARGS__)
#define serial_receive(...)     BBOS_CONTROL_DEVICE(P8X32_SERIAL, serial_receive, __VA_ARGS__)

/* Include I/O control interface */
#include "p8x32_serial_control.h"

/* Include I/O manager interface */
#include "p8x32_serial_manager.h"

