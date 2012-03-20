/*
 * The "Blink me who I am" test run on specified cog and flush
 * correspond LED on Propeller Demo Board.
 *
 * Copyright (c) 2012 Sladeware LLC
 */

#include <bb/os/drivers/processors/propeller_p8x32/config.h>
#include <bb/os/drivers/processors/propeller_p8x32/pins.h>
#include <bb/os/drivers/processors/propeller_p8x32/sio.h>
#include <bb/os/drivers/processors/propeller_p8x32/delay.h>

int
main()
{
  while (1)
    {
      /* Flush LED that corresponds to active cog. */
      propeller_set_dira_bits(1 << (16 + cogid()));
      propeller_set_outa_bits(1 << (16 + cogid()));
      bbos_delay_msec(500); /* wait... */

      propeller_clr_dira_bits(1 << (16 + cogid()));
      propeller_clr_outa_bits(1 << (16 + cogid()));
      bbos_delay_msec(500); /* wait... */

      sio_cogsafe_printf("Cog %d is running!\n", propeller_cogid());
    }

  return 0;
}
