/*
 * Propeller Demo Board (PDB) board-specific setup.
 *
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos/env.h>
#include <bbos/hardware/device/driver/led.h>
#include <bbos/hardware/platform/P8X32A-Q44/pins.h>
#include <catalina_cog.h>

#define BOARD_NUMBER_OF_LEDS 8
#define BIT(n) (1<<(n))

/*
 * Pin assignments:
 *
 * P0-P31 : gpio.
 * P31    : Rx from host (gpio after boot up).
 * P30    : Tx to host (gpio after boot up/download).
 * P29    : I2C SDA connection to external EEPROM (gpio after boot up).
 * P28    : I2C SCL connection to external EEPROM (gpio after boot up).
 * Vdd    : 3.3 V power (2.7 - 3.6 VDC).
 * Vss    : Ground (0 VDC).
 * BOEn   : Brown Out Enable (active low). Must be connected to either Vdd or
          : Vss. If low, RESn becomes a weak output (~5 K?) for monitoring
          : purposes but can be driven low to cause reset. If high, RESn is a
          : CMOS input with Schmitt Trigger.
 * RESn   : Reset (active low). When low, resets the Propeller chip; all cogs
          : disabled and I/O pins floating. Propeller restarts 50 ms after RESn
          : transitions from low to high.
 * XI     : Crystal / clock input. Can connect to crystal or oscillator.
 * XO     : Crystal Output. Provides feedback for an external crystal.
          : Internal C and R selectable for crystals (no other components required).
 */

static struct gpio_led_info board_led_list[] = {
  { GPIO_PIN_PA(16), },
  { GPIO_PIN_PA(17), },
  { GPIO_PIN_PA(18), },
  { GPIO_PIN_PA(19), },
  { GPIO_PIN_PA(20), },
  { GPIO_PIN_PA(21), },
  { GPIO_PIN_PA(22), },
  { GPIO_PIN_PA(23), },
};

static struct gpio_led_platform_data board_led_data = {
  BOARD_NUMBER_OF_LEDS,
  board_led_list
};

//static struct platform_device board_led_device = {
//  .device = {
//    .platform_data = &board_led_data,
//  },
//};

/**
 * board_init_leds - Initialize LEDs.
 */
void
board_init_leds()
{
  uint16_t i;

  for (i=0; i<BOARD_NUMBER_OF_LEDS; i++) {
    _dira(BIT(board_led_list[i].gpio), BIT(board_led_list[i].gpio));
    _outa(BIT(board_led_list[i].gpio), BIT(board_led_list[i].gpio));
    _outa(BIT(board_led_list[i].gpio), 0);
    //_dira(BIT(board_led_list[i].gpio), BIT(board_led_list[i].gpio));
  }

  // register device
}

/**
 * board_init - Initialize Propeller Demo Board.
 */
bbos_return_t
board_init()
{
  board_init_leds();

  return BBOS_SUCCESS;
}

