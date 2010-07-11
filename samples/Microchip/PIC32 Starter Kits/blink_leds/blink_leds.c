/*
 * Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
 */

#include <bbos.h>
#include <plib.h>

#define SYS_FREQ (80000000)

// prototype
void DelayMs(unsigned int);

bbos_return_t
led_switcher(bbos_thread_id_t tid)
{
  switch(tid) {
    case LED0_ID:
	  DelayMs(100);
	  mPORTDToggleBits(BIT_0); // toggle LED0 (same as LATDINV = 0x0001)
      break;

    case LED1_ID:
	  DelayMs(100);
	  mPORTDToggleBits(BIT_1); // toggle LED1 (same as LATDINV = 0x0002)
      break;

    case LED2_ID:
	  DelayMs(100);
      mPORTDToggleBits(BIT_2); // toggle LED2 (same as LATDINV = 0x0004)
      break;
  } 

  return BBOS_SUCCESS;
}

//  blink_leds application code
int main(void)
{
  bbos_init();

  // Turn off leds before configuring the IO pin as output
  mPORTDClearBits(BIT_0 | BIT_1 | BIT_2);             // same as LATDCLR = 0x0007

  // Set RD0, RD1 and RD2 as outputs
  mPORTDSetPinsDigitalOut(BIT_0 | BIT_1 | BIT_2 );    // same as TRISDCLR = 0x0007

  //Initialize the DB_UTILS IO channel
  DBINIT();
	
	// Display a message using db_utils
  DBPRINTF("Welcome to the PIC32 Blink Leds example. \n");
  DBPRINTF("This example demonstrates a simple method to toggle LEDs. \n");

  bbos_thread_start(LED0_ID);
  bbos_thread_start(LED1_ID);
  bbos_thread_start(LED2_ID);

  bbos_start();

  return 0;
}


/******************************************************************************
*	DelayMs()
*
*	This functions provides a software millisecond delay
******************************************************************************/
void DelayMs(unsigned int msec)
{
	unsigned int tWait, tStart;

    tWait=(SYS_FREQ/2000)*msec;
    tStart=ReadCoreTimer();
    while((ReadCoreTimer()-tStart)<tWait);		// wait for the time to pass
}


